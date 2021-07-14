use findfood;
--
-- SELECT *
-- FROM diners;

-- SELECT id from diners table which is duplicated,
-- Uncomment block below to examine duplicated records.
--
--  SELECT id FROM (SELECT id, ROW_NUMBER()   
--        OVER (PARTITION BY name, address, city, district, pricemin, pricemax, website, qualityPoint, pricePoint, servicePoint, destinationPoint, spacePoint
-- 			ORDER BY name) AS row_num   
--     FROM diners) AS temp_table WHERE row_num > 1;
-- 

-- DELETE duplicated in menu
DELETE FROM menu 
WHERE dinerID IN (  
    SELECT id FROM (
		SELECT id, ROW_NUMBER()   
		OVER (
			PARTITION BY name, address, city, district, pricemin, pricemax, website, qualityPoint, pricePoint, servicePoint, destinationPoint, spacePoint
			ORDER BY name) AS row_num   
		FROM diners) AS temp_table 
	WHERE row_num > 1);
--

-- DELETE duplicated in timetable
DELETE FROM timetable 
WHERE dinerID IN (  
     SELECT id FROM (
		SELECT id, ROW_NUMBER()   
		OVER (
			PARTITION BY name, address, city, district, pricemin, pricemax, website, qualityPoint, pricePoint, servicePoint, destinationPoint, spacePoint
			ORDER BY name) AS row_num   
		FROM diners) AS temp_table 
	WHERE row_num > 1);
--

-- DELETE duplicated in diners
DELETE FROM diners 
WHERE id IN (  
	SELECT id FROM (
		SELECT id, ROW_NUMBER()   
		OVER (
			PARTITION BY name, address, city, district, pricemin, pricemax, website, qualityPoint, pricePoint, servicePoint, destinationPoint, spacePoint
			ORDER BY name) AS row_num   
		FROM diners) AS temp_table 
	WHERE row_num > 1);
--