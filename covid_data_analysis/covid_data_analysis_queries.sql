-- Queries for the Data Exploration
-- WE ARE ONLY TALKING ABOUT COUNTRIES HENCE EXCL. (WORLD, ASIA, AFRICA, etc...) WHICH ARE THERE IN DATA

-- First let's look at then important columns
SELECT location, date, population, total_cases, total_deaths
FROM coviddeaths ORDER BY 1, 2;


-- Country with highest record cases
SELECT location, MAX(total_cases) AS Cases
FROM coviddeaths
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY MAX(total_cases) DESC;


-- Continent with highest record cases
SELECT continent, MAX(total_cases) AS Cases
FROM coviddeaths
GROUP BY continent
ORDER BY MAX(total_cases) DESC;


-- Death over total cases in %
SELECT location, date, population, total_cases, total_deaths, (total_deaths / total_cases)*100 deathpercent
FROM coviddeaths; 
-- GIVES ROUGH ESTIMATE OF CHANCES OF DEATH IF ONE GETS INFECTED


-- Cases over total population in %
SELECT location, date, population, total_cases, total_deaths, (total_cases / population)*100 infectionpercent
FROM coviddeaths
WHERE location LIKE '%States'
ORDER BY 1,2;


-- COUNTRY WITH HIGHEST INFECTION RATE
SELECT location, MAX(population), MAX(total_cases), MAX((total_cases/population))*100 AS INFECTIONRATE
FROM coviddeaths 
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY 4 DESC;


-- COUNTRY WITH HIGHEST DEATH RATE
SELECT location, MAX(population) POP, MAX(total_cases) CASES, MAX(total_deaths) DEATHS, (MAX(total_deaths/total_cases))*100 AS DEATHRATE
FROM coviddeaths 
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY 5 DESC;


-- Worldwide DeathRate per day
SELECT date, SUM(new_cases) cases, SUM(new_deaths) deaths,
	CASE
		WHEN SUM(new_cases) <> 0 THEN SUM(new_deaths)/SUM(new_cases)
		WHEN SUM(new_cases) = 0 THEN 0
	END DeathRate
FROM coviddeaths
WHERE continent IS NOT NULL
GROUP BY date
ORDER BY date;


-- EXPLORING BOTH TABLES TOGETHER BY Joining 2 tables

-- Vaccine over Population of each country in %
SELECT d.location, MAX(population) population, MAX(total_vaccinations) vacc,
(MAX(total_vaccinations) / MAX(population))*100 VaccPercent
FROM coviddeaths d
JOIN covidvaccine v
ON d.location = v.location
AND d.date = v.date
WHERE d.continent IS NOT NULL
GROUP BY d.location;


-- Rolling total (Cumulative) of vaccinations each day
WITH VaccinationRate (Location, Date, Population, NewVaccination, RollingTotal)
AS(
	SELECT d.location, d.date, d.population, v.new_vaccinations,
	SUM(v.new_vaccinations) OVER(PARTITION BY d.location ORDER BY d.location, d.date) as RollingTotal
	FROM coviddeaths d
	JOIN covidvaccine v
	ON d.location = v.location
	AND d.date = v.date
	WHERE d.continent IS NOT NULL
)

SELECT *, (RollingTotal/Population)*100 VaccRate FROM VaccinationRate;

-- CREATING VIEWS
CREATE VIEW VaccRate AS(
	WITH VaccinationRate (Location, Date, Population, NewVaccination, RollingTotal)
	AS(
		SELECT d.location, d.date, d.population, v.new_vaccinations,
		SUM(v.new_vaccinations) OVER(PARTITION BY d.location ORDER BY d.location, d.date) as RollingTotal
		FROM coviddeaths d
		JOIN covidvaccine v
		ON d.location = v.location
		AND d.date = v.date
		WHERE d.continent IS NOT NULL
	)

	SELECT *, (RollingTotal/Population)*100 VaccRate FROM VaccinationRate
);


































