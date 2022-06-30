/*getting the modules */
const express = require("express");
const ejs = require("ejs");
const path = require("path");

var TfIdf = require('node-tfidf');
var tfidf = new TfIdf();
const fs = require('fs');

/* Reading our database files */
var fs1 = require("fs");
var texturl = fs1.readFileSync("Problems/Problem_urls.txt", "utf-8");
var urltext = texturl.split("\n");

var fs2 = require("fs");
var texttitle = fs2.readFileSync("Problems/Problem_titles.txt", "utf-8");
var titletext = texttitle.split("\n");

/* setting up server */
const app = express();
app.use(express.json());
app.set("view engine", "ejs");
app.use(express.static(path.join(__dirname, "/public")));
const PORT = process.env.PORT || 3000;

/* GET Requests */
app.get("/", (req, res) => {
    res.render("index");
});

app.get("/home", (req, res) => {
    res.render("index");
});

app.get("/search", (req, res) => {
    const query = req.query;
    const question = query.question;

    const mapQ = new Map();
    var flag = 0;
    
    /* loading text data of each document into tfidf */
    for (let i = 1; i <= 1436; i++) {
        tfidf.addFileSync(`Problems/Problem_texts/problem_text${i}.txt`);
    }

    let txt = [];

    for (let i = 1; i <= 1436; i++) {
        let data = fs.readFileSync(`Problems/Problem_texts/problem_text${i}.txt`, 'utf-8');
        txt.push(data);
    }

    /* finding the similarity of Question query with each document's text data loaded in tfidf */
    tfidf.tfidfs(question, function (i, measure) {
        mapQ.set(i + 1, measure);
    });
    const sortedNumDesc = new Map([...mapQ].sort((a, b) => b[1] - a[1]));

    let data_array = [];
    /* Creating top 5 similar problems */
    for (const [key, value] of sortedNumDesc.entries()) {
        if (flag < 5 && value != 0) {
            let my_object = {
                title: titletext[key - 1],
                url: urltext[key - 1],
                statement: txt[key - 1]
            };
            flag += 1;
            data_array.push(my_object);
        }
        else {
            break;
        }
    }

    setTimeout(() => {
        res.json(data_array);
    }, 3000);
});

app.listen(PORT, () => {
    console.log("Server is running on port " + PORT);
});