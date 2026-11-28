import json
import logging
import re
import time
import xml.etree.ElementTree as ET
import httpx

logger = logging.getLogger(__name__)

CHANNEL_ID = 'UChlDg9qBmP_JlwQ1_2by5kQ'
RSS_URL = f'https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}'
CHANNEL_VIDEOS_URL = f'https://www.youtube.com/channel/{CHANNEL_ID}/videos'
BROWSER_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
MAX_ITEMS = 15  # RSS 와 같은 개수
CACHE_SECONDS = 600  # 10분

NS = {
    'atom': 'http://www.w3.org/2005/Atom',
    'yt': 'http://www.youtube.com/xml/schemas/2015',
    'media': 'http://search.yahoo.com/mrss/',
}

_cache = {'at': 0.0, 'items': []}

def _parse(xml_text: str) -> list:
    root = ET.fromstring(xml_text)
    items = []
    for entry in root.findall('atom:entry', NS):
        video_id = entry.findtext('yt:videoId', default='', namespaces=NS)
        link = entry.find('atom:link', NS)
        items.append({
            'video_id': video_id,
            'title': entry.findtext('atom:title', default='', namespaces=NS),
            'link': link.get('href') if link is not None else f'https://www.youtube.com/watch?v={video_id}',
            'thumbnail': f'https://i.ytimg.com/vi/{video_id}/mqdefault.jpg',
            'published': entry.findtext('atom:published', default='', namespaces=NS),
        })
    return items

def _find_videos(node, out: list):
    """채널 페이지 데이터에서 영상 항목(lockupViewModel / videoRenderer)을 순서대로 모음"""
    if isinstance(node, dict):
        lockup = node.get('lockupViewModel')
        if isinstance(lockup, dict) and lockup.get('contentType') == 'LOCKUP_CONTENT_TYPE_VIDEO':
            title = (((lockup.get('metadata') or {}).get('lockupMetadataViewModel') or {}).get('title') or {}).get('content', '')
            out.append((lockup.get('contentId', ''), title))
            return
        renderer = node.get('videoRenderer')
        if isinstance(renderer, dict) and renderer.get('videoId'):
            title = ''.join(run.get('text', '') for run in (renderer.get('title') or {}).get('runs', []))
            out.append((renderer['videoId'], title))
            return
        for value in node.values():
            _find_videos(value, out)
    elif isinstance(node, list):
        for value in node:
            _find_videos(value, out)

def _parse_channel_page(html: str) -> list:
    """채널 '동영상' 페이지의 ytInitialData 에서 최신 영상 목록 (게시일은 페이지에 없어 비워 둠)"""
    match = re.search(r'var ytInitialData = (\{.*?\});</script>', html, re.S)
    if not match:
        raise ValueError('채널 페이지에서 영상 정보를 찾지 못했습니다.')
    found: list = []
    _find_videos(json.loads(match.group(1)), found)
    items, seen = [], set()
    for video_id, title in found:
        if not video_id or video_id in seen:
            continue
        seen.add(video_id)
        items.append({
            'video_id': video_id,
            'title': title,
            'link': f'https://www.youtube.com/watch?v={video_id}',
            'thumbnail': f'https://i.ytimg.com/vi/{video_id}/mqdefault.jpg',
            'published': '',
        })
    if not items:
        raise ValueError('채널 페이지에 영상이 없습니다.')
    return items[:MAX_ITEMS]

async def _fetch(client: httpx.AsyncClient) -> list:
    # RSS 가 기본. 유튜브 RSS 가 오류(503 등)를 내는 때가 있어 실패하면 채널 동영상 페이지에서 읽음
    try:
        res = await client.get(RSS_URL)
        res.raise_for_status()
        return _parse(res.text)
    except Exception as e:
        logger.warning('유튜브 RSS 실패, 채널 페이지로 대신 조회: %s', e)
    res = await client.get(CHANNEL_VIDEOS_URL, headers={'Accept-Language': 'ko-KR,ko', 'User-Agent': BROWSER_UA})
    res.raise_for_status()
    return _parse_channel_page(res.text)

async def get_latest_videos() -> list:
    """유튜브 채널 최신 영상(최대 15개)을 서버에서 가져와 10분간 캐시합니다."""
    if _cache['items'] and time.time() - _cache['at'] < CACHE_SECONDS:
        return _cache['items']
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            items = await _fetch(client)
        _cache.update(at=time.time(), items=items)
        return items
    except Exception:
        logger.exception('유튜브 최신 영상 조회 실패')
        # 유튜브 일시 오류 시 이전 캐시라도 반환
        if _cache['items']:
            return _cache['items']
        raise
