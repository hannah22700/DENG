-- Kontroverse Votes mit knappem Ausgang
SELECT "BusinessTitle", "IdVote",
       COUNT(CASE WHEN "DecisionText" = 'Nein' THEN 1 END) as no_votes,
       ABS(COUNT(CASE WHEN "DecisionText" = 'Ja' THEN 1 END) - 
           COUNT(CASE WHEN "DecisionText" = 'Nein' THEN 1 END)) as margin
FROM voting
GROUP BY "BusinessTitle", "IdVote"
ORDER BY margin ASC
LIMIT 20;
