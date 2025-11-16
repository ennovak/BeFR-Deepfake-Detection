const express = require("express");
const multer = require("multer");
const fs = require("fs");
const app = express();

app.use(express.static("public"));  // your website folder

// Where uploaded images will be saved
const storage = multer.diskStorage({
    destination: "reports/images for reports/",
    filename: (req, file, cb) => {
        cb(null, Date.now() + "-" + file.originalname);
    }
});

const upload = multer({ storage: storage });

// Handle the report submit
app.post("/report-error", upload.single("image"), (req, res) => {
    const message = req.body.message;
    const image = req.file ? req.file.filename : "No image uploaded";
    const timestamp = new Date().toLocaleString();

    const logEntry = `
===========================
Time: ${timestamp}
Message: ${message}
Image: ${image}
===========================

`;

    // Save log entry
    fs.appendFileSync("reports/reports.log", logEntry);

    res.status(200).send("Report received");
});

app.listen(3000, () => console.log("Server running on port 3000"));
