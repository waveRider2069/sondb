CREATE OR REPLACE VIEW projs_search AS
SELECT sproj.idr_proj idr,group_concat(pp.idp) idps, group_concat(pp.abbr) abbrs
FROM sub_projects sproj
       JOIN projects pp ON pp.idp = sproj.idp_proj
GROUP BY sproj.idr_proj;

CREATE OR REPLACE VIEW tests_search AS
SELECT stest.idr_test idr, group_concat(tests.idt) idts, group_concat(tests.test_name) tnames
FROM sub_tests stest
       JOIN tests ON stest.idt_test = tests.idt
GROUP BY stest.idr_test;

CREATE OR REPLACE VIEW tests_tag AS
SELECT stest.idr_test idr, tests.idt, tests.test_name tname
FROM sub_tests stest
       JOIN tests ON stest.idt_test = tests.idt;

# CREATE OR REPLACE VIEW subs_search AS
# SELECT ids_rec           ids,
#        idr,
#        group_concat(idr) idrs,
#        subname,
#        age,
#        phone,
#        gender,
#        attitude,
#        location,
#        spare,
#        sparenote,
#        comments,
#        air_avgr,
#        air_levelr,
#        air_avgl,
#        air_levell,
#        cause_right,
#        cause_left,
#        shape_right,
#        shape_left,
#        immittance_right,
#        immittance_left
# FROM sub_records
# GROUP BY ids_rec
# ORDER BY update_time;


# ids_rec                                            ids,
#        idr                                                idr,
#        group_concat(idr)                                  idrs,
#        group_concat(date_format(record_time, '%Y-%m-%d')) rdates,
#        date_format(record_time, '%Y-%m-%d')               rdate,
#        subname,
#        age,
#        phone,
#        gender,
#        attitude,
#        location,
#        spare,
#        sparenote,
#        comments,
#        air_avgr,
#        air_levelr,
#        air_avgl,
#        air_levell,
#        bone_avgr,
#        bone_levelr,
#        bone_avgl,
#        bone_levell,
#        cause_right,
#        cause_left,
#        shape_right,
#        shape_left,
#        immittance_right,
#        immittance_left,
#        idts,
#        tnames,
#        idps,
#        abbrs
# CREATE OR REPLACE VIEW subs_search AS
# SELECT *
# FROM (SELECT rec.*,
#              tests.idts   idts,
#              tests.tnames tnames,
#              projs.idps   idps,
#              projs.abbrs  abbrs
#       FROM sub_records rec
#              LEFT JOIN projs_search projs on projs.idr = rec.idr
#       ORDER BY rec.record_time DESC
#       LIMIT 100000) sub_inform
# GROUP BY ids_rec;
