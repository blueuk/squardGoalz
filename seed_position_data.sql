-- ============================================================
-- 포지션 공통코드 등록 (common_cd_b)
-- ============================================================
INSERT INTO common_cd_b (group_cd, code, code_name, code_seq, use_yn, create_id, create_dt, update_id, update_dt)
VALUES
  ('position_cd', 'FIX', '픽소',    1, 'Y', 'system', NOW(), 'system', NOW()),
  ('position_cd', 'PIV', '피보',    2, 'Y', 'system', NOW(), 'system', NOW()),
  ('position_cd', 'ALA', '아라',    3, 'Y', 'system', NOW(), 'system', NOW()),
  ('position_cd', 'GOL', '골레이로', 4, 'Y', 'system', NOW(), 'system', NOW()),
  ('position_cd', 'CEN', '센트로',  5, 'Y', 'system', NOW(), 'system', NOW())
ON CONFLICT (group_cd, code) DO UPDATE SET code_name = EXCLUDED.code_name, use_yn = 'Y', update_dt = NOW();

-- ============================================================
-- 포지션 가중치 등록 (position_point_b)
-- ============================================================
-- GOL (골레이로)
INSERT INTO position_point_b (position_cd, score_cd, position_val, create_id, create_dt, update_id, update_dt) VALUES
  ('GOL','001',0.008,'system',NOW(),'system',NOW()),
  ('GOL','002',0.008,'system',NOW(),'system',NOW()),
  ('GOL','003',0.023,'system',NOW(),'system',NOW()),
  ('GOL','004',0.008,'system',NOW(),'system',NOW()),
  ('GOL','005',0.008,'system',NOW(),'system',NOW()),
  ('GOL','006',0.023,'system',NOW(),'system',NOW()),
  ('GOL','007',0.115,'system',NOW(),'system',NOW()),
  ('GOL','008',0.057,'system',NOW(),'system',NOW()),
  ('GOL','009',0.115,'system',NOW(),'system',NOW()),
  ('GOL','010',0.008,'system',NOW(),'system',NOW()),
  ('GOL','011',0.008,'system',NOW(),'system',NOW()),
  ('GOL','012',0.115,'system',NOW(),'system',NOW()),
  ('GOL','013',0.008,'system',NOW(),'system',NOW()),
  ('GOL','014',0.023,'system',NOW(),'system',NOW()),
  ('GOL','015',0.115,'system',NOW(),'system',NOW()),
  ('GOL','016',0.023,'system',NOW(),'system',NOW()),
  ('GOL','017',0.008,'system',NOW(),'system',NOW()),
  ('GOL','018',0.008,'system',NOW(),'system',NOW()),
  ('GOL','019',0.008,'system',NOW(),'system',NOW()),
  ('GOL','020',0.002,'system',NOW(),'system',NOW()),
  ('GOL','021',0.008,'system',NOW(),'system',NOW()),
  ('GOL','022',0.008,'system',NOW(),'system',NOW()),
  ('GOL','023',0.057,'system',NOW(),'system',NOW()),
  ('GOL','024',0.057,'system',NOW(),'system',NOW()),
  ('GOL','025',0.057,'system',NOW(),'system',NOW()),
  ('GOL','026',0.008,'system',NOW(),'system',NOW()),
  ('GOL','027',0.057,'system',NOW(),'system',NOW()),
  ('GOL','028',0.057,'system',NOW(),'system',NOW())
ON CONFLICT (position_cd, score_cd) DO UPDATE SET position_val = EXCLUDED.position_val, update_dt = NOW();

-- FIX (픽소)
INSERT INTO position_point_b (position_cd, score_cd, position_val, create_id, create_dt, update_id, update_dt) VALUES
  ('FIX','001',0.043,'system',NOW(),'system',NOW()),
  ('FIX','002',0.043,'system',NOW(),'system',NOW()),
  ('FIX','003',0.017,'system',NOW(),'system',NOW()),
  ('FIX','004',0.006,'system',NOW(),'system',NOW()),
  ('FIX','005',0.043,'system',NOW(),'system',NOW()),
  ('FIX','006',0.043,'system',NOW(),'system',NOW()),
  ('FIX','007',0.043,'system',NOW(),'system',NOW()),
  ('FIX','008',0.017,'system',NOW(),'system',NOW()),
  ('FIX','009',0.087,'system',NOW(),'system',NOW()),
  ('FIX','010',0.087,'system',NOW(),'system',NOW()),
  ('FIX','011',0.043,'system',NOW(),'system',NOW()),
  ('FIX','012',0.087,'system',NOW(),'system',NOW()),
  ('FIX','013',0.087,'system',NOW(),'system',NOW()),
  ('FIX','014',0.043,'system',NOW(),'system',NOW()),
  ('FIX','015',0.006,'system',NOW(),'system',NOW()),
  ('FIX','016',0.017,'system',NOW(),'system',NOW()),
  ('FIX','017',0.087,'system',NOW(),'system',NOW()),
  ('FIX','018',0.006,'system',NOW(),'system',NOW()),
  ('FIX','019',0.006,'system',NOW(),'system',NOW()),
  ('FIX','020',0.008,'system',NOW(),'system',NOW()),
  ('FIX','021',0.006,'system',NOW(),'system',NOW()),
  ('FIX','022',0.006,'system',NOW(),'system',NOW()),
  ('FIX','023',0.043,'system',NOW(),'system',NOW()),
  ('FIX','024',0.043,'system',NOW(),'system',NOW()),
  ('FIX','025',0.043,'system',NOW(),'system',NOW()),
  ('FIX','026',0.006,'system',NOW(),'system',NOW()),
  ('FIX','027',0.017,'system',NOW(),'system',NOW()),
  ('FIX','028',0.017,'system',NOW(),'system',NOW())
ON CONFLICT (position_cd, score_cd) DO UPDATE SET position_val = EXCLUDED.position_val, update_dt = NOW();

-- ALA (아라)
INSERT INTO position_point_b (position_cd, score_cd, position_val, create_id, create_dt, update_id, update_dt) VALUES
  ('ALA','001',0.006,'system',NOW(),'system',NOW()),
  ('ALA','002',0.092,'system',NOW(),'system',NOW()),
  ('ALA','003',0.092,'system',NOW(),'system',NOW()),
  ('ALA','004',0.092,'system',NOW(),'system',NOW()),
  ('ALA','005',0.006,'system',NOW(),'system',NOW()),
  ('ALA','006',0.004,'system',NOW(),'system',NOW()),
  ('ALA','007',0.046,'system',NOW(),'system',NOW()),
  ('ALA','008',0.046,'system',NOW(),'system',NOW()),
  ('ALA','009',0.018,'system',NOW(),'system',NOW()),
  ('ALA','010',0.018,'system',NOW(),'system',NOW()),
  ('ALA','011',0.018,'system',NOW(),'system',NOW()),
  ('ALA','012',0.006,'system',NOW(),'system',NOW()),
  ('ALA','013',0.006,'system',NOW(),'system',NOW()),
  ('ALA','014',0.018,'system',NOW(),'system',NOW()),
  ('ALA','015',0.006,'system',NOW(),'system',NOW()),
  ('ALA','016',0.006,'system',NOW(),'system',NOW()),
  ('ALA','017',0.018,'system',NOW(),'system',NOW()),
  ('ALA','018',0.092,'system',NOW(),'system',NOW()),
  ('ALA','019',0.046,'system',NOW(),'system',NOW()),
  ('ALA','020',0.046,'system',NOW(),'system',NOW()),
  ('ALA','021',0.046,'system',NOW(),'system',NOW()),
  ('ALA','022',0.046,'system',NOW(),'system',NOW()),
  ('ALA','023',0.046,'system',NOW(),'system',NOW()),
  ('ALA','024',0.006,'system',NOW(),'system',NOW()),
  ('ALA','025',0.046,'system',NOW(),'system',NOW()),
  ('ALA','026',0.092,'system',NOW(),'system',NOW()),
  ('ALA','027',0.018,'system',NOW(),'system',NOW()),
  ('ALA','028',0.018,'system',NOW(),'system',NOW())
ON CONFLICT (position_cd, score_cd) DO UPDATE SET position_val = EXCLUDED.position_val, update_dt = NOW();

-- PIV (피보)
INSERT INTO position_point_b (position_cd, score_cd, position_val, create_id, create_dt, update_id, update_dt) VALUES
  ('PIV','001',0.099,'system',NOW(),'system',NOW()),
  ('PIV','002',0.099,'system',NOW(),'system',NOW()),
  ('PIV','003',0.020,'system',NOW(),'system',NOW()),
  ('PIV','004',0.007,'system',NOW(),'system',NOW()),
  ('PIV','005',0.006,'system',NOW(),'system',NOW()),
  ('PIV','006',0.006,'system',NOW(),'system',NOW()),
  ('PIV','007',0.050,'system',NOW(),'system',NOW()),
  ('PIV','008',0.050,'system',NOW(),'system',NOW()),
  ('PIV','009',0.099,'system',NOW(),'system',NOW()),
  ('PIV','010',0.006,'system',NOW(),'system',NOW()),
  ('PIV','011',0.006,'system',NOW(),'system',NOW()),
  ('PIV','012',0.006,'system',NOW(),'system',NOW()),
  ('PIV','013',0.006,'system',NOW(),'system',NOW()),
  ('PIV','014',0.006,'system',NOW(),'system',NOW()),
  ('PIV','015',0.007,'system',NOW(),'system',NOW()),
  ('PIV','016',0.050,'system',NOW(),'system',NOW()),
  ('PIV','017',0.006,'system',NOW(),'system',NOW()),
  ('PIV','018',0.007,'system',NOW(),'system',NOW()),
  ('PIV','019',0.050,'system',NOW(),'system',NOW()),
  ('PIV','020',0.050,'system',NOW(),'system',NOW()),
  ('PIV','021',0.099,'system',NOW(),'system',NOW()),
  ('PIV','022',0.099,'system',NOW(),'system',NOW()),
  ('PIV','023',0.050,'system',NOW(),'system',NOW()),
  ('PIV','024',0.006,'system',NOW(),'system',NOW()),
  ('PIV','025',0.020,'system',NOW(),'system',NOW()),
  ('PIV','026',0.050,'system',NOW(),'system',NOW()),
  ('PIV','027',0.020,'system',NOW(),'system',NOW()),
  ('PIV','028',0.020,'system',NOW(),'system',NOW())
ON CONFLICT (position_cd, score_cd) DO UPDATE SET position_val = EXCLUDED.position_val, update_dt = NOW();

-- CEN (센트로)
INSERT INTO position_point_b (position_cd, score_cd, position_val, create_id, create_dt, update_id, update_dt) VALUES
  ('CEN','001',0.006,'system',NOW(),'system',NOW()),
  ('CEN','002',0.049,'system',NOW(),'system',NOW()),
  ('CEN','003',0.049,'system',NOW(),'system',NOW()),
  ('CEN','004',0.006,'system',NOW(),'system',NOW()),
  ('CEN','005',0.006,'system',NOW(),'system',NOW()),
  ('CEN','006',0.006,'system',NOW(),'system',NOW()),
  ('CEN','007',0.049,'system',NOW(),'system',NOW()),
  ('CEN','008',0.020,'system',NOW(),'system',NOW()),
  ('CEN','009',0.098,'system',NOW(),'system',NOW()),
  ('CEN','010',0.020,'system',NOW(),'system',NOW()),
  ('CEN','011',0.049,'system',NOW(),'system',NOW()),
  ('CEN','012',0.020,'system',NOW(),'system',NOW()),
  ('CEN','013',0.006,'system',NOW(),'system',NOW()),
  ('CEN','014',0.020,'system',NOW(),'system',NOW()),
  ('CEN','015',0.006,'system',NOW(),'system',NOW()),
  ('CEN','016',0.007,'system',NOW(),'system',NOW()),
  ('CEN','017',0.006,'system',NOW(),'system',NOW()),
  ('CEN','018',0.006,'system',NOW(),'system',NOW()),
  ('CEN','019',0.098,'system',NOW(),'system',NOW()),
  ('CEN','020',0.049,'system',NOW(),'system',NOW()),
  ('CEN','021',0.006,'system',NOW(),'system',NOW()),
  ('CEN','022',0.006,'system',NOW(),'system',NOW()),
  ('CEN','023',0.098,'system',NOW(),'system',NOW()),
  ('CEN','024',0.049,'system',NOW(),'system',NOW()),
  ('CEN','025',0.098,'system',NOW(),'system',NOW()),
  ('CEN','026',0.020,'system',NOW(),'system',NOW()),
  ('CEN','027',0.098,'system',NOW(),'system',NOW()),
  ('CEN','028',0.049,'system',NOW(),'system',NOW())
ON CONFLICT (position_cd, score_cd) DO UPDATE SET position_val = EXCLUDED.position_val, update_dt = NOW();

