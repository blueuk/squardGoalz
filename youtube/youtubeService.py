import time
import xml.etree.ElementTree as ET
import httpx

CHANNEL_ID = 'UChlDg9qBmP_JlwQ1_2by5kQ'
RSS_URL = f'https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}'
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

async def get_latest_videos() -> list:
    """유튜브 채널 RSS(최근 15개)를 서버에서 가져와 10분간 캐시합니다."""
    if _cache['items'] and time.time() - _cache['at'] < CACHE_SECONDS:
        return _cache['items']
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(RSS_URL)
            res.raise_for_status()
        items = _parse(res.text)
        _cache.update(at=time.time(), items=items)
        return items
    except Exception:
        # 유튜브 일시 오류 시 이전 캐시라도 반환
        if _cache['items']:
            return _cache['items']
        raise
