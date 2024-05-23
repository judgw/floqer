const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');

const app = express();
const port = 3000;

app.use(cors());

// Connect to SQLite database
const db = new sqlite3.Database('database.sqlite', (err) => {
    if (err) {
        console.error('Could not connect to database', err);
    } else {
        console.log('Connected to database');
    }
});

// Route to get data from MAIN_TABLE
app.get('/main_table', (req, res) => {
    const query = 'SELECT * FROM MAIN_TABLE';
    db.all(query, [], (err, rows) => {
        if (err) {
            res.status(400).json({ error: err.message });
            return;
        }
        res.json({ data: rows });
    });
});

// Route to get data from the corresponding yearly table
app.get('/data', (req, res) => {
    const year = req.query.year;
    const tableName = `Data_${year}`;
    const query = `SELECT * FROM ${tableName}`;
    db.all(query, [], (err, rows) => {
        if (err) {
            res.status(400).json({ error: err.message });
            return;
        }
        res.json({ data: rows });
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
