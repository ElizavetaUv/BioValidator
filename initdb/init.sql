CREATE TYPE variant_type AS ENUM ('SNP', 'Somatic', 'Indel', 'Other');
CREATE TYPE allele AS ENUM ('A', 'C', 'G', 'T', 'N');

CREATE SCHEMA main;

-- CREATE TABLE genes (
--     id ID PRIMARY KEY,

--     Chromosome INT2 CHECK (Chromosome >= 1 AND Chromosome <= 22),
--     Start_Position INT4 NOT NULL,
--     End_Position INT4 NOT NULL
-- );

CREATE TABLE  main.mutations (
    id ID PRIMARY KEY,
    Hugo_Symbol VARCHAR(50) NOT NULL,
    Variant_Type variant_type NOT NULL,
    Reference_Allele allele NOT NULL,
    Allele VARCHAR(50),
    Chromosome,
    Start_Position,
    End_Position,
);