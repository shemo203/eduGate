DROP TABLE IF EXISTS SubmissionDocument;
DROP TABLE IF EXISTS Submission;
DROP TABLE IF EXISTS Document;
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Admin;

CREATE TABLE Student(
    studentID INTEGER PRIMARY KEY,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL
);

CREATE TABLE Admin(
    adminID INTEGER PRIMARY KEY,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL
);

CREATE TABLE Submission(
    submissionID INTEGER PRIMARY KEY,
    created_at DATETIME NOT NULL,
    score INTEGER,
    AIstatus TEXT,
    studentID INTEGER NOT NULL,
    adminID INTEGER NOT NULL,
    FOREIGN KEY(studentID) REFERENCES Student(studentID),
    FOREIGN KEY(adminID) REFERENCES Admin(adminID)
);

CREATE TABLE Document(
    documentID INTEGER PRIMARY KEY,
    filetype TEXT NOT NULL,
    size INTEGER
);

CREATE TABLE SubmissionDocument(
    submissionID INTEGER NOT NULL,
    documentID INTEGER NOT NULL,
    FOREIGN KEY (submissionID) REFERENCES Submission(submissionID),
    FOREIGN KEY (documentID) REFERENCES Document(documentID),
    PRIMARY KEY(submissionID, documentID)
);


