set foreign_key_checks = 1;
set explicit_defaults_for_timestamp = ON;

#  Procedures;
DELIMITER $$
DROP PROCEDURE IF EXISTS insert_projects $$
CREATE PROCEDURE insert_projects(pidu_proj VARCHAR(18),
                                 pidp VARCHAR(16),
                                 ptitle VARCHAR(128),
                                 pabbr VARCHAR(64),
                                 pleader VARCHAR(32),
                                 pstart_time DATETIME,
                                 pdueto_end DATETIME,
                                 pstate VARCHAR(16),
                                 pbudget INT,
                                 psubjectn INT,
                                 pvisits INT,
                                 pdescription VARCHAR(500),
                                 precord_time DATETIME,
                                 pupdate_time DATETIME)

BEGIN
  INSERT INTO projects
  VALUES (pidu_proj, pidp, ptitle, pabbr, pleader, pstart_time, pdueto_end, pstate, pbudget, psubjectn, pvisits,
          pdescription, precord_time, pupdate_time);
END $$

DELIMITER $$
DROP PROCEDURE IF EXISTS update_projects $$
CREATE PROCEDURE update_projects(pidu_proj VARCHAR(18),
                                 pidp VARCHAR(16),
                                 ptitle VARCHAR(128),
                                 pabbr VARCHAR(64),
                                 pleader VARCHAR(32),
                                 pstart_time DATETIME,
                                 pdueto_end DATETIME,
                                 pstate VARCHAR(16),
                                 pbudget INT,
                                 psubjectn INT,
                                 pvisits INT,
                                 pdescription VARCHAR(500),
                                 pupdate_time DATETIME)

BEGIN
  update projects
  set title=ptitle,
      abbr=pabbr,
      leader=pleader,
      start_time=pstart_time,
      dueto_end=pdueto_end,
      state=pstate,
      budget=pbudget,
      subjectn=psubjectn,
      visits=pvisits,
      description=pdescription,
      update_time = pupdate_time
  WHERE idp = pidp
    AND BINARY idu_proj = pidu_proj;
END $$
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS insert_sub_records $$
CREATE PROCEDURE insert_sub_records(pidu_rec VARCHAR(18),
                                    pidr VARCHAR(16),
                                    pids_rec VARCHAR(16),
                                    precord_time DATETIME,
                                    pupdate_time DATETIME,
                                    psubname VARCHAR(32),
                                    page_record TINYINT,
                                    page TINYINT,
                                    pphone VARCHAR(64),
                                    pgender VARCHAR(8),
                                    pattitude VARCHAR(16),
                                    plocation VARCHAR(32),
                                    pspare VARCHAR(16),
                                    psparenote VARCHAR(64),
                                    paidwearing VARCHAR(16),
                                    pdiseases VARCHAR(128),
                                    pcomments VARCHAR(1024),
                                    pair_125r SMALLINT,
                                    pair_250r SMALLINT,
                                    pair_500r SMALLINT,
                                    pair_750r SMALLINT,
                                    pair_1000r SMALLINT,
                                    pair_1500r SMALLINT,
                                    pair_2000r SMALLINT,
                                    pair_3000r SMALLINT,
                                    pair_4000r SMALLINT,
                                    pair_6000r SMALLINT,
                                    pair_8000r SMALLINT,
                                    pair_avgr FLOAT,
                                    pair_levelr VARCHAR(16),
                                    pair_125l SMALLINT,
                                    pair_250l SMALLINT,
                                    pair_500l SMALLINT,
                                    pair_750l SMALLINT,
                                    pair_1000l SMALLINT,
                                    pair_1500l SMALLINT,
                                    pair_2000l SMALLINT,
                                    pair_3000l SMALLINT,
                                    pair_4000l SMALLINT,
                                    pair_6000l SMALLINT,
                                    pair_8000l SMALLINT,
                                    pair_avgl FLOAT,
                                    pair_levell VARCHAR(16),
                                    pbone_125r SMALLINT,
                                    pbone_250r SMALLINT,
                                    pbone_500r SMALLINT,
                                    pbone_750r SMALLINT,
                                    pbone_1000r SMALLINT,
                                    pbone_1500r SMALLINT,
                                    pbone_2000r SMALLINT,
                                    pbone_3000r SMALLINT,
                                    pbone_4000r SMALLINT,
                                    pbone_6000r SMALLINT,
                                    pbone_8000r SMALLINT,
                                    pbone_avgr FLOAT,
                                    pbone_levelr VARCHAR(16),
                                    pbone_125l SMALLINT,
                                    pbone_250l SMALLINT,
                                    pbone_500l SMALLINT,
                                    pbone_750l SMALLINT,
                                    pbone_1000l SMALLINT,
                                    pbone_1500l SMALLINT,
                                    pbone_2000l SMALLINT,
                                    pbone_3000l SMALLINT,
                                    pbone_4000l SMALLINT,
                                    pbone_6000l SMALLINT,
                                    pbone_8000l SMALLINT,
                                    pbone_avgl FLOAT,
                                    pbone_levell VARCHAR(16),
                                    pcause_right VARCHAR(16),
                                    pcause_left VARCHAR(16),
                                    pshape_right VARCHAR(16),
                                    pshape_left VARCHAR(16),
                                    pimmittance_right VARCHAR(8),
                                    pimmittance_left VARCHAR(8),
                                    pspeech VARCHAR(16))
BEGIN
  INSERT INTO sub_records
  VALUES (pidu_rec, pidr, pids_rec, precord_time, pupdate_time, psubname, page_record, page, pphone, pgender, pattitude,
          plocation, pspare, psparenote, paidwearing, pdiseases, pcomments,
          pair_125r,pair_250r, pair_500r,pair_750r, pair_1000r,pair_1500r,pair_2000r,pair_3000r,pair_4000r,pair_6000r, pair_8000r, pair_avgr, pair_levelr,
          pair_125l,pair_250l, pair_500l,pair_750l, pair_1000l,pair_1500l,pair_2000l,pair_3000l,pair_4000l,pair_6000l, pair_8000l, pair_avgl, pair_levell,
          pbone_125r,pbone_250r,pbone_500r,pbone_750r,pbone_1000r,pbone_1500r,pbone_2000r, pbone_3000r, pbone_4000r, pbone_6000r,pbone_8000r,pbone_avgr, pbone_levelr,
          pbone_125l,pbone_250l,pbone_500l,pbone_750l,pbone_1000l,pbone_1500l,pbone_2000l, pbone_3000l, pbone_4000l, pbone_6000l,pbone_8000l,pbone_avgl, pbone_levell,
          pcause_right, pcause_left, pshape_right, pshape_left, pimmittance_right,
          pimmittance_left,
          pspeech);
END $$

DROP PROCEDURE IF EXISTS update_sub_records $$
CREATE PROCEDURE update_sub_records(pidu_rec VARCHAR(18),
                                    pidr VARCHAR(16),
                                    pupdate_time DATETIME,
                                    psubname VARCHAR(32),
                                    page_record TINYINT,
                                    page TINYINT,
                                    pphone VARCHAR(64),
                                    pgender VARCHAR(8),
                                    pattitude VARCHAR(16),
                                    plocation VARCHAR(32),
                                    pspare VARCHAR(16),
                                    psparenote VARCHAR(64),
                                    paidwearing VARCHAR(16),
                                    pdiseases VARCHAR(128),
                                    pcomments VARCHAR(1024),
                                    pair_125r SMALLINT,
                                    pair_250r SMALLINT,
                                    pair_500r SMALLINT,
                                    pair_750r SMALLINT,
                                    pair_1000r SMALLINT,
                                    pair_1500r SMALLINT,
                                    pair_2000r SMALLINT,
                                    pair_3000r SMALLINT,
                                    pair_4000r SMALLINT,
                                    pair_6000r SMALLINT,
                                    pair_8000r SMALLINT,
                                    pair_avgr FLOAT,
                                    pair_levelr VARCHAR(16),
                                    pair_125l SMALLINT,
                                    pair_250l SMALLINT,
                                    pair_500l SMALLINT,
                                    pair_750l SMALLINT,
                                    pair_1000l SMALLINT,
                                    pair_1500l SMALLINT,
                                    pair_2000l SMALLINT,
                                    pair_3000l SMALLINT,
                                    pair_4000l SMALLINT,
                                    pair_6000l SMALLINT,
                                    pair_8000l SMALLINT,
                                    pair_avgl FLOAT,
                                    pair_levell VARCHAR(16),
                                    pbone_125r SMALLINT,
                                    pbone_250r SMALLINT,
                                    pbone_500r SMALLINT,
                                    pbone_750r SMALLINT,
                                    pbone_1000r SMALLINT,
                                    pbone_1500r SMALLINT,
                                    pbone_2000r SMALLINT,
                                    pbone_3000r SMALLINT,
                                    pbone_4000r SMALLINT,
                                    pbone_6000r SMALLINT,
                                    pbone_8000r SMALLINT,
                                    pbone_avgr FLOAT,
                                    pbone_levelr VARCHAR(16),
                                    pbone_125l SMALLINT,
                                    pbone_250l SMALLINT,
                                    pbone_500l SMALLINT,
                                    pbone_750l SMALLINT,
                                    pbone_1000l SMALLINT,
                                    pbone_1500l SMALLINT,
                                    pbone_2000l SMALLINT,
                                    pbone_3000l SMALLINT,
                                    pbone_4000l SMALLINT,
                                    pbone_6000l SMALLINT,
                                    pbone_8000l SMALLINT,
                                    pbone_avgl FLOAT,
                                    pbone_levell VARCHAR(16),
                                    pcause_right VARCHAR(16),
                                    pcause_left VARCHAR(16),
                                    pshape_right VARCHAR(16),
                                    pshape_left VARCHAR(16),
                                    pimmittance_right VARCHAR(8),
                                    pimmittance_left VARCHAR(8),
                                    pspeech VARCHAR(16))
BEGIN
  update sub_records
  set update_time=pupdate_time,
      subname=psubname,
      age_record=page_record,
      age=page,
      phone=pphone,
      gender=pgender,
      attitude=pattitude,
      location=plocation,
      spare=pspare,
      sparenote=psparenote,
      aidwearing=paidwearing,
      diseases=pdiseases,
      comments=pcomments,
      air_125r=pair_125r,
      air_250r=pair_250r,
      air_500r=pair_500r,
      air_750r=pair_750r,
      air_1000r=pair_1000r,
      air_1500r=pair_1500r,
      air_2000r=pair_2000r,
      air_3000r=pair_3000r,
      air_4000r=pair_4000r,
      air_6000r=pair_6000r,
      air_8000r=pair_8000r,
      air_avgr=pair_avgr,
      air_levelr=pair_levelr,
      air_125l=pair_125l,
      air_250l=pair_250l,
      air_500l=pair_500l,
      air_750l=pair_750l,
      air_1000l=pair_1000l,
      air_1500l=pair_1500l,
      air_2000l=pair_2000l,
      air_3000l=pair_3000l,
      air_4000l=pair_4000l,
      air_6000l=pair_6000l,
      air_8000l=pair_8000l,
      air_avgl=pair_avgl,
      air_levell=pair_levell,
      air_125r=pbone_125r,
      bone_250r=pbone_250r,
      bone_500r=pbone_500r,
      bone_750r=pbone_750r,
      bone_1000r=pbone_1000r,
      bone_1500r=pbone_1500r,
      bone_2000r=pbone_2000r,
      bone_3000r=pbone_3000r,
      bone_4000r=pbone_4000r,
      bone_6000r=pbone_6000r,
      bone_8000r=pbone_8000r,
      bone_avgr=pbone_avgr,
      bone_levelr=pbone_levelr,
      air_125l=pbone_125l,
      bone_250l=pbone_250l,
      bone_500l=pbone_500l,
      bone_750l=pbone_750l,
      bone_1000l=pbone_1000l,
      bone_1500l=pbone_1500l,
      bone_2000l=pbone_2000l,
      bone_3000l=pbone_3000l,
      bone_4000l=pbone_4000l,
      bone_6000l=pbone_6000l,
      bone_8000l=pbone_8000l,
      bone_avgl=pbone_avgl,
      bone_levell=pbone_levell,
      cause_right=pcause_right,
      cause_left=pcause_left,
      shape_right=pshape_right,
      shape_left=pshape_left,
      immittance_right=pimmittance_right,
      immittance_left=pimmittance_left,
      speech = pspeech
  where idr = pidr
    AND BINARY idu_rec = pidu_rec;

END $$
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS cal_thresh $$
CREATE PROCEDURE cal_thresh()
BEGIN
  UPDATE sub_records
  SET air_avgr=(air_500r + air_1000r + air_2000r + air_4000r) / 4,
      air_avgl=(air_500l + air_1000l + air_2000l + air_4000l) / 4,
      bone_avgr=(bone_500r + bone_1000r + bone_2000r + bone_4000r) / 4,
      bone_avgl=(bone_500l + bone_1000l + bone_2000l + bone_4000l) / 4;
END $$

DROP PROCEDURE IF EXISTS set_level $$
CREATE PROCEDURE set_level()
BEGIN
  UPDATE sub_records
  SET air_levelr=CASE
                   WHEN air_avgr <= 20 THEN 'normal'
                   WHEN air_avgr <= 40 THEN 'mild'
                   WHEN air_avgr <= 55 THEN 'medium'
                   WHEN air_avgr <= 70 THEN 'medium-severe'
                   WHEN air_avgr <= 90 THEN 'severe'
                   ELSE 'profound' END;
END $$

DROP PROCEDURE IF EXISTS insert_sub_projects $$
CREATE PROCEDURE insert_sub_projects(pidr_proj VARCHAR(16), pidp_proj VARCHAR(12))
BEGIN
  REPLACE INTO sub_projects (idr_proj, idp_proj) VALUES (pidr_proj, pidp_proj);
END $$


DROP PROCEDURE IF EXISTS insert_sub_tests;
CREATE PROCEDURE insert_sub_tests(pidr_test VARCHAR(16), pidp_test VARCHAR(12))
BEGIN
  REPLACE INTO sub_projects (idr_test, idp_test) VALUES (pidr_test, pidp_test);
END $$



DROP FUNCTION IF EXISTS if_delayed $$
CREATE FUNCTION if_delayed(endt DATE, state VARCHAR(16)) RETURNS VARCHAR(16) DETERMINISTIC
BEGIN
  DECLARE dstate VARCHAR(16);
  IF state = 'in progress' THEN
    IF endt < current_date THEN
      SET dstate = 'delayed';
      RETURN (dstate);
    ELSE
      RETURN (state);
    END IF;
  ELSE
    RETURN (state);
  END IF;
END $$

DELIMITER $$

DROP PROCEDURE IF EXISTS search_subs_earliest $$
CREATE PROCEDURE search_subs_earliest()
BEGIN
  SELECT ids_rec                                            ids,
         idr                                                idr,
         group_concat(idr)                                  idrs,
         group_concat(date_format(record_time, '%Y-%m-%d')) rdates,
         date_format(record_time, '%Y-%m-%d')               rdate,
         subname,
         age,
         phone,
         gender,
         attitude,
         location,
         spare,
         sparenote,
         comments,
         air_avgr,
         air_levelr,
         air_avgl,
         air_levell,
         bone_avgr,
         bone_levelr,
         bone_avgl,
         bone_levell,
         cause_right,
         cause_left,
         shape_right,
         shape_left,
         immittance_right,
         immittance_left
  FROM (SELECT * FROM sub_records ORDER BY record_time DESC LIMIT 100000) ordered_rec
  WHERE idr LIKE 'R%'
  GROUP BY ids
  ORDER BY update_time ASC;
END $$
DELIMITER ;

DELIMITER $$


DROP PROCEDURE IF EXISTS search_subs_latest $$
CREATE PROCEDURE search_subs_latest()
BEGIN
  SELECT ids_rec                                            ids,
         idr                                                idr,
         group_concat(idr)                                  idrs,
         group_concat(date_format(record_time, '%Y-%m-%d')) rdates,
         date_format(record_time, '%Y-%m-%d')               rdate,
         subname,
         age,
         phone,
         gender,
         attitude,
         location,
         spare,
         sparenote,
         comments,
         air_avgr,
         air_levelr,
         air_avgl,
         air_levell,
         bone_avgr,
         bone_levelr,
         bone_avgl,
         bone_levell,
         cause_right,
         cause_left,
         shape_right,
         shape_left,
         immittance_right,
         immittance_left
  FROM (SELECT * FROM sub_records ORDER BY record_time DESC LIMIT 100000) ordered_rec
  WHERE idr LIKE 'R%'
  GROUP BY ids
  ORDER BY update_time DESC;
END $$

DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS search_subs_asc $$
CREATE PROCEDURE search_subs_asc(IN sort varchar(4))
BEGIN
  SELECT ids_rec                                            ids,
         idr                                                idr,
         group_concat(idr)                                  idrs,
         group_concat(date_format(record_time, '%Y-%m-%d')) rdates,
         date_format(record_time, '%Y-%m-%d')               rdate,
         subname,
         age,
         phone,
         gender
  FROM (SELECT * FROM sub_records ORDER BY record_time DESC LIMIT 100000) ordered_rec
  WHERE idr LIKE 'R%'
  GROUP BY ids
  ORDER BY CASE sort
             WHEN '2' THEN update_time
             WHEN '4' THEN greatest(coalesce(air_avgl, 0), coalesce(air_avgr, 0), coalesce(bone_avgl, 0),
                                    coalesce(bone_avgr, 0)) END ASC;
END $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS search_subs $$
CREATE PROCEDURE search_subs(IN startfrom SMALLINT, IN pagesize SMALLINT, IN cidu VARCHAR(18), IN sort VARCHAR(4),
                             ckeys VARCHAR(128), clevel VARCHAR(64),
                             ccause VARCHAR(32), cshape VARCHAR(32),
                             csymmetry VARCHAR(32), cspeech VARCHAR(32), cgender VARCHAR(16), cattitude VARCHAR(32),
                             clocation VARCHAR(64), cspare VARCHAR(32), teststr VARCHAR(512), ageDw TINYINT,
                             ageUp TINYINT,
                             f250aUp SMALLINT, f500aUp SMALLINT, f1000aUp SMALLINT, f2000aUp SMALLINT,
                             f4000aUp SMALLINT, f8000aUp SMALLINT,
                             f250bUp SMALLINT, f500bUp SMALLINT, f1000bUp SMALLINT, f2000bUp SMALLINT,
                             f4000bUp SMALLINT, f8000bUp SMALLINT,
                             f250aDw SMALLINT, f500aDw SMALLINT, f1000aDw SMALLINT, f2000aDw SMALLINT,
                             f4000aDw SMALLINT, f8000aDw SMALLINT,
                             f250bDw SMALLINT, f500bDw SMALLINT, f1000bDw SMALLINT, f2000bDw SMALLINT,
                             f4000bDw SMALLINT, f8000bDw SMALLINT)
BEGIN
  DROP TABLE IF EXISTS subs_search;
  CREATE TEMPORARY TABLE subs_search (SELECT rec.ids_rec                              ids,
                                             rec.idr,
                                             date_format(rec.record_time, '%Y-%m-%d') rdate,
                                             rec.update_time,
                                             rec.subname,
                                             rec.age,
                                             rec.phone,
                                             rec.gender,
                                             rec.attitude,
                                             rec.location,
                                             rec.spare,
                                             rec.sparenote,
                                             rec.diseases,
                                             rec.comments,
                                             rec.air_avgr,
                                             rec.air_levelr,
                                             rec.air_avgl,
                                             rec.air_levell,
                                             rec.bone_avgr,
                                             rec.bone_levelr,
                                             rec.bone_avgl,
                                             rec.bone_levell,
                                             rec.cause_right,
                                             rec.cause_left,
                                             rec.shape_right,
                                             rec.shape_left,
                                             rec.immittance_right,
                                             rec.immittance_left,
                                             rec.speech,
                                             projs.idps,
                                             projs.abbrs
                                      FROM sub_records rec
                                             LEFT JOIN projs_search projs ON projs.idr = rec.idr
                                      WHERE BINARY idu_rec = cidu
                                        AND if(length(clevel),
                                               find_in_set(air_levelr, clevel) OR find_in_set(air_levell, clevel), 1)
                                        AND if(length(ccause),
                                               find_in_set(cause_right, ccause) OR find_in_set(cause_left, ccause), 1)
                                        AND if(length(cshape),
                                               find_in_set(shape_right, cshape) OR find_in_set(shape_left, cshape), 1)
                                        AND CASE csymmetry
                                              WHEN 'symmetric' THEN abs(air_avgl - air_avgr) <= 15
                                              WHEN 'asymmetric' THEN abs(air_avgl - air_avgr) > 15
                                              ELSE 1 END
                                        AND if(length(cspeech), find_in_set(speech, cspeech), 1)
                                        AND CASE cgender
                                              WHEN 'M' THEN gender = 'M'
                                              WHEN 'F' THEN gender = 'F'
                                              ELSE 1 END
                                        AND if(length(cattitude), find_in_set(attitude, cattitude), 1)
                                        AND if(length(clocation), find_in_set(location, clocation), 1)
                                        AND if(length(cspare), find_in_set(spare, cspare), 1)
                                        AND if(length(teststr), rec.idr IN (SELECT * from t_tags), 1)
                                        AND if(ageDw <=> NULL, 1, age >= ageDw)
                                        AND if(ageUp <=> NULL, 1, age <= ageUp)
                                        AND if(f250aUp <=> NULL, 1, rec.air_250r <= f250aUp OR rec.air_250l <= f250aUp)
                                        AND if(f500aUp <=> NULL, 1, rec.air_500r <= f500aUp OR rec.air_500l <= f500aUp)
                                        AND if(f1000aUp <=> NULL, 1,
                                               rec.air_1000r <= f1000aUp OR rec.air_1000l <= f1000aUp)
                                        AND if(f2000aUp <=> NULL, 1,
                                               rec.air_2000r <= f2000aUp OR rec.air_2000l <= f2000aUp)
                                        AND if(f4000aUp <=> NULL, 1,
                                               rec.air_4000r <= f4000aUp OR rec.air_4000l <= f4000aUp)
                                        AND if(f8000aUp <=> NULL, 1,
                                               rec.air_8000r <= f8000aUp OR rec.air_8000l <= f8000aUp)
                                        AND if(f250bUp <=> NULL, 1,
                                               rec.bone_250r <= f250bUp OR rec.bone_250l <= f250bUp)
                                        AND if(f500bUp <=> NULL, 1,
                                               rec.bone_500r <= f500bUp OR rec.bone_500l <= f500bUp)
                                        AND if(f1000bUp <=> NULL, 1,
                                               rec.bone_1000r <= f1000bUp OR rec.bone_1000l <= f1000bUp)
                                        AND if(f2000bUp <=> NULL, 1,
                                               rec.bone_2000r <= f2000bUp OR rec.bone_2000l <= f2000bUp)
                                        AND if(f4000bUp <=> NULL, 1,
                                               rec.bone_4000r <= f4000bUp OR rec.bone_4000l <= f4000bUp)
                                        AND if(f8000bUp <=> NULL, 1,
                                               rec.bone_8000r <= f8000bUp OR rec.bone_8000l <= f8000bUp)
                                        AND if(f250aDw <=> NULL, 1, rec.air_250r >= f250aDw OR rec.air_250l >= f250aDw)
                                        AND if(f500aDw <=> NULL, 1, rec.air_500r >= f500aDw OR rec.air_500l >= f500aDw)
                                        AND if(f1000aDw <=> NULL, 1,
                                               rec.air_1000r >= f1000aDw OR rec.air_1000l >= f1000aDw)
                                        AND if(f2000aDw <=> NULL, 1,
                                               rec.air_2000r >= f2000aDw OR rec.air_2000l >= f2000aDw)
                                        AND if(f4000aDw <=> NULL, 1,
                                               rec.air_4000r >= f4000aDw OR rec.air_4000l >= f4000aDw)
                                        AND if(f8000aDw <=> NULL, 1,
                                               rec.air_8000r >= f8000aDw OR rec.air_8000l >= f8000aDw)
                                        AND if(f250bDw <=> NULL, 1,
                                               rec.bone_250r >= f250bDw OR rec.bone_250l >= f250bDw)
                                        AND if(f500bDw <=> NULL, 1,
                                               rec.bone_500r >= f500bDw OR rec.bone_500r >= f500bDw)
                                        AND if(f1000bDw <=> NULL, 1,
                                               rec.bone_1000r >= f1000bDw OR rec.bone_1000l >= f1000bDw)
                                        AND if(f2000bDw <=> NULL, 1,
                                               rec.bone_2000r >= f2000bDw OR rec.bone_2000l >= f2000bDw)
                                        AND if(f4000bDw <=> NULL, 1,
                                               rec.bone_4000r >= f4000bDw OR rec.bone_4000l >= f4000bDw)
                                        AND if(f8000bDw <=> NULL, 1,
                                               rec.bone_8000r >= f8000bDw OR rec.bone_8000l >= f8000bDw)
                                      ORDER BY rec.record_time DESC);

  ALTER TABLE subs_search
    ENGINE = myisam;
  ALTER TABLE subs_search
    convert to character set utf8;
  ALTER TABLE subs_search
    ADD FULLTEXT INDEX ft_name_sparenote (subname, sparenote) WITH PARSER ngram;
  ALTER TABLE subs_search
    ADD FULLTEXT INDEX ft_diseases_comments (diseases, comments) WITH PARSER ngram;

  #   SELECT count(*)
  #   from (select *
  #         FROM subs_search
  #         WHERE if(ckeys != '', match(subname, sparenote) against(ckeys) OR match(diseases, diseases) against(ckeys), 1)
  #         GROUP BY ids) grouped;

  SELECT count(DISTINCT ids)
  FROM subs_search
  WHERE if(ckeys != '', match(subname, sparenote) against(ckeys) OR match(diseases, diseases) against(ckeys), 1);

  SELECT *,group_concat(rdate) rdates,group_concat(idr) idrs
  FROM subs_search
  WHERE if(ckeys != '', match(subname, sparenote) against(ckeys) OR match(diseases, diseases) against(ckeys), 1)
  GROUP BY ids
  ORDER BY
    CASE sort WHEN '1' THEN update_time end DESC,
    CASE sort WHEN '2' THEN update_time end ASC,
    CASE sort
      WHEN '3' THEN greatest(coalesce(air_avgl, 0), coalesce(air_avgr, 0), coalesce(bone_avgl, 0),
                             coalesce(bone_avgr, 0)) end DESC,
    CASE sort
      WHEN '4' THEN greatest(coalesce(air_avgl, 0), coalesce(air_avgr, 0), coalesce(bone_avgl, 0),
                             coalesce(bone_avgr, 0)) end ASC
  LIMIT pagesize OFFSET startfrom;

END $$
DELIMITER ;


DELIMITER $$
DROP PROCEDURE IF EXISTS search_subs_proj $$
CREATE PROCEDURE search_subs_proj(IN iduc VARCHAR(18), IN sort VARCHAR(4), IN idpc VARCHAR(16), IN statec VARCHAR(20))
BEGIN
  DROP TABLE IF EXISTS subs_search_proj;
  CREATE TEMPORARY TABLE subs_search_proj (SELECT rec.ids_rec                              ids,
                                                  rec.idr,
                                                  date_format(rec.record_time, '%Y-%m-%d') rdate,
                                                  rec.update_time,
                                                  rec.subname,
                                                  rec.age,
                                                  rec.phone,
                                                  rec.gender,
                                                  rec.attitude,
                                                  rec.location,
                                                  rec.spare,
                                                  rec.sparenote,
                                                  rec.diseases,
                                                  rec.comments,
                                                  rec.air_avgr,
                                                  rec.air_levelr,
                                                  rec.air_avgl,
                                                  rec.air_levell,
                                                  rec.bone_avgr,
                                                  rec.bone_levelr,
                                                  rec.bone_avgl,
                                                  rec.bone_levell,
                                                  rec.cause_right,
                                                  rec.cause_left,
                                                  rec.shape_right,
                                                  rec.shape_left,
                                                  rec.immittance_right,
                                                  rec.immittance_left,
                                                  rec.speech,
                                                  projs.idps,
                                                  projs.abbrs
                                           FROM (SELECT * FROM sub_records WHERE BINARY idu_rec = iduc) rec
                                                  JOIN (SELECT idr_proj
                                                        FROM sub_projects
                                                        WHERE idp_proj = idpc
                                                          AND find_in_set(isfinish, statec)) subprojs
                                                       ON rec.idr = subprojs.idr_proj
                                                  LEFT JOIN projs_search projs ON projs.idr = rec.idr)
                                                  ORDER BY rec.record_time DESC;

  SELECT *,group_concat(rdate) rdates,group_concat(idr) idrs
  FROM subs_search_proj
  GROUP BY ids
  order by
    CASE sort WHEN '1' THEN update_time end DESC,
    CASE sort WHEN '2' THEN update_time end ASC,
    CASE sort
      WHEN '3' THEN greatest(coalesce(air_avgl, 0), coalesce(air_avgr, 0), coalesce(bone_avgl, 0),
                             coalesce(bone_avgr, 0)) end DESC,
    CASE sort
      WHEN '4' THEN greatest(coalesce(air_avgl, 0), coalesce(air_avgr, 0), coalesce(bone_avgl, 0),
                             coalesce(bone_avgr, 0)) end ASC;
END $$
DELIMITER ;

# greatest(coalesce(air_avgl, 0), coalesce(air_avgr, 0), coalesce(bone_avgl, 0),
#                                       coalesce(bone_avgr, 0)) END DESC;
delimiter $$
drop procedure if exists aggregate $$
create procedure aggregate(IN cuser VARCHAR(18), IN cstate VARCHAR(16))
BEGIN
  #   DROP TABLE IF EXISTS temp1;
  DROP TABLE IF EXISTS temp1;
  DROP TABLE IF EXISTS temp2;
  DROP TABLE IF EXISTS temptemp;
  CREATE TEMPORARY TABLE temp1 (SELECT subp.idp_proj, subp.payment, subr.idr, subr.ids_rec
                                FROM (SELECT idr,ids_rec,record_time FROM sub_records WHERE BINARY idu_rec = cuser) subr
                                       JOIN sub_projects subp
                                            ON subr.idr = subp.idr_proj
                                ORDER BY subr.record_time DESC);
  ALTER TABLE temp1
    ADD INDEX idp_proj_name (idp_proj);
  ALTER TABLE temp1
    ADD INDEX idr_name (idr);

  CREATE TEMPORARY TABLE temptemp (SELECT idr FROM temp1 GROUP BY ids_rec);

  CREATE TEMPORARY TABLE temp2 (SELECT ps.idp,
                                       ps.abbr,
                                       ps.title,
                                       ps.leader,
                                       ps.start_time                      start,
                                       ps.dueto_end                       endt,
                                       if_delayed(ps.dueto_end, ps.state) state,
                                       ps.budget,
                                       ps.subjectn,
                                       ifnull(sub.payment, 0)             pay,
                                       sub.idr
                                FROM (select *
                                      from projects
                                      where BINARY idu_proj = cuser) ps
                                       LEFT JOIN (select *
                                                  from temp1
                                                  where idr in (select idr from temptemp)) sub
                                                 on ps.idp = sub.idp_proj
                                WHERE
                                  CASE cstate
                                    WHEN 'delayed' THEN ps.state = 'in progress' and ps.dueto_end < current_date
                                    WHEN 'in progress'
                                      THEN ps.state = 'in progress' and ps.dueto_end >= current_date
                                    WHEN 'all' THEN 1
                                    ELSE ps.state = cstate END);

  SELECT *,if(isnull(temp2.idr), 0, count(*)) totaln,sum(temp2.pay) totalp
  FROM temp2
  GROUP BY idp
  ORDER BY abbr = 'TBD', start DESC;
END $$
DELIMITER ;
# call aggregate('SonovaRd', 'all');

DELIMITER $$
drop procedure if exists aggregate_single $$
create procedure aggregate_single(IN cuser VARCHAR(18), IN cidp VARCHAR(16))
BEGIN
  DROP TABLE IF EXISTS temp1;
  DROP TABLE IF EXISTS temp2;
  DROP TABLE IF EXISTS temptemp;
  CREATE TEMPORARY TABLE temp1 (SELECT subp.idp_proj, subp.payment, subr.idr, subr.ids_rec
                                FROM (SELECT idr,ids_rec,record_time FROM sub_records WHERE BINARY idu_rec = cuser) subr
                                       JOIN sub_projects subp
                                            ON subr.idr = subp.idr_proj
                                ORDER BY subr.record_time DESC);
  ALTER TABLE temp1
    ADD INDEX idr_name (idr);

  CREATE TEMPORARY TABLE temptemp (SELECT idr FROM temp1 GROUP BY ids_rec);

  CREATE TEMPORARY TABLE temp2 (SELECT ps.idp,
                                       ps.abbr,
                                       ps.title,
                                       ps.leader,
                                       ps.start_time                      start,
                                       ps.dueto_end                       endt,
                                       if_delayed(ps.dueto_end, ps.state) state,
                                       ps.budget,
                                       ps.subjectn,
                                       ps.visits,
                                       ps.description,
                                       ifnull(sub.payment, 0)             pay,
                                       sub.idr
                                FROM (select *
                                      from projects
                                      where BINARY idu_proj = cuser
                                        AND idp = cidp) ps
                                       LEFT JOIN (select *
                                                  from temp1
                                                  where idr in (select idr from temptemp)) sub
                                                 on ps.idp = sub.idp_proj);

  SELECT *,if(isnull(temp2.idr), 0, count(*)) totaln,sum(temp2.pay) totalp
  FROM temp2
  GROUP BY idp
  ORDER BY abbr = 'TBD', start DESC;
END $$
DELIMITER ;

# call aggregate_single('SonovaRd', 'P90a5524dee30');
delete from sub_ids Where ids in (SELECT ids_rec FROM sub_records WHERE idr in (SELECT idr_proj FROM sub_projects WHERE idp_proj='P63f438360b94'));

