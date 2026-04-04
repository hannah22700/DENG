
-- Rebels - Parteimitglieder, welche nicht im Zuge ihrer Partei stimmen
SELECT v."ParlGroupName", v."PersonNumber", v."FirstName", v."LastName",
       COUNT(*) as total_votes,
       SUM(CASE WHEN v."DecisionText" = ps."DecisionText" THEN 1 ELSE 0 END) as aligned,
       ROUND(100.0 * SUM(CASE WHEN v."DecisionText" = ps."DecisionText" THEN 1 ELSE 0 END) / COUNT(*), 1) as discipline_pct
FROM voting v
JOIN partysummary ps ON v."IdVote" = ps."IdVote" AND v."ParlGroupName" = ps."ParlGroupName"
GROUP BY v."ParlGroupName", v."PersonNumber", v."FirstName", v."LastName"
HAVING COUNT(*) > 10
ORDER BY discipline_pct asc -- könnte auch desc sein, hier ordnen wir nach Rebels 
LIMIT 100;