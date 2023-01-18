// packages import
const express = require("express");
const app = express();
const cors = require("cors");
const axios = require("axios");

app.use(cors());

const port = process.env.PORT || 8080;

app.get("/", (req, res) => {
    // Get parameters type and id from the request. They are strings and mandatory
    const { type, id } = req.query;
    if (!type || !id) {
        res.status(400).send("Missing parameters id or/and type");
        return;
    }

    console.log(`Request received for ${type} with id ${id} from ${req.ip}`)

    const backendUrl = type === "quizizz" ? `https://quizizz.com/quiz/${id}` : `https://kahoot.it/v2/quiz/${id}`;
    axios.get(backendUrl).then(response => res.send(response.data));
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});