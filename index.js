const express = require('express');
const { MongoClient } = require('mongodb');

const app = express();
const port = process.env.PORT || 3000;

const MONGO_URI = "mongodb+srv://rajmukherjee1601:0dBZfnllyiAvmRtj@cluster0.grwr7ep.mongodb.net/?retryWrites=true&w=majority";
const client = new MongoClient(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true });

app.use(express.json());

let db

async function connectToDatabase() {
    try {
        await client.connect();
        db = client.db('Plotline');
        console.log('Connected to MongoDB');
    } catch (err) {
        console.error('Error connecting to MongoDB:', err);
    }
}

connectToDatabase();

function calculateTax(price) {
    if (price > 5000) {
        return price * 0.18;  // Tax PB
    } else if (1000 < price <= 5000) {
        return price * 0.12;  // Tax PA
    } else {
        return 200;  // Tax PC
    }
}
function calculateServiceTax(price) {
    if (price > 8000) {
        return price * 0.15;  // Tax SB
    } else if (1000 < price <= 8000) {
        return price * 0.10;  // Tax SA
    } else {
        return 100;  // Tax SC
    }
}


app.post('/signup', async (req, res) => {
    const collection = db.collection('User_login');
    try {
        const data = req.body;
        if (data) {
            await collection.insertOne(data);
            res.status(201).json({ message: 'User added successfully' });
        } else {
            res.status(400).json({ message: 'No data provided' });
        }
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

app.post('/product/insert', async (req, res) => {
    const collection = db.collection('product');
    try {
        const data = req.body;
        if (data) {
            await collection.insertOne(data);
            res.status(201).json({ message: 'Data inserted successfully' });
        } else {
            res.status(400).json({ message: 'No data provided' });
        }
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

app.post('/service/insert', async (req, res) => {
    const collection = db.collection('Service');
    try {
        const data = req.body;
        if (data) {
            await collection.insertOne(data);
            res.status(201).json({ message: 'Data inserted successfully' });
        } else {
            res.status(400).json({ message: 'No data provided' });
        }
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

app.get('/product/retrieve', async (req, res) => {
    const collection = db.collection('product');
    try {
        const users = await collection.find({}).toArray();
        if (users.length > 0) {
            const result = users.map(user => ({
                name: user.Name,
                price: user.price
            }));
            res.status(200).json({ users: result });
        } else {
            res.status(404).json({ message: 'No data found in database' });
        }
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

// Define other routes similarly
app.get('/service/retrieve', async (req, res) => {
    const collection = db.collection('Service');
    try {
        const users = await collection.find({}).toArray();
        if (users.length > 0) {
            const result = users.map(user => ({
                name: user.Name,
                price: user.price
            }));
            res.status(200).json({ users: result });
        } else {
            res.status(404).json({ message: 'No data found in database' });
        }
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});
app.post('/product/remove', async (req, res) => {
    const collection = db.collection('product');
    try {
        const users = await collection.find({}).toArray();
        const userNames = users.map(user => user.Name);

        const data = req.body;
        console.log(data.Name);
        console.log(userNames);

        if (data.Name && userNames.includes(data.Name)) {
            const result = await collection.deleteOne({ Name: data.Name });
            if (result.deletedCount > 0) {
                res.status(200).json({ message: 'Data removed successfully' });
            } else {
                res.status(404).json({ message: 'No matching data found' });
            }
        } else {
            res.status(400).json({ message: "Missing 'name' field in request data" });
        }
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});
app.post('/service/remove', async (req, res) => {
    const collection = db.collection('Service');
    try {
        const users = await collection.find({}).toArray();
        const userNames = users.map(user => user.Name);

        const data = req.body;
        console.log(data.Name);
        console.log(userNames);

        if (data.Name && userNames.includes(data.Name)) {
            const result = await collection.deleteOne({ Name: data.Name });
            if (result.deletedCount > 0) {
                res.status(200).json({ message: 'Data removed successfully' });
            } else {
                res.status(404).json({ message: 'No matching data found' });
            }
        } else {
            res.status(400).json({ message: "Missing 'name' field in request data" });
        }
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});
app.delete('/product/clear', async (req, res) => {
    const collection = db.collection('product');
    try {
        const result = await collection.deleteMany({});
        res.status(200).json({ message: `${result.deletedCount} documents deleted` });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

app.delete('/service/clear', async (req, res) => {
    const collection = db.collection('Service');
    try {
        const result = await collection.deleteMany({});
        res.status(200).json({ message: `${result.deletedCount} documents deleted` });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});
app.get('/product/calculate_bill', async (req, res) => {
    const collection = db.collection('product');
    try {
        const products = await collection.find({}).toArray();
        let totalBill = 0;

        products.forEach(product => {
            const price = product.price;
            const tax = calculateTax(price);
            const totalPrice = price + tax;
            totalBill += totalPrice;
        });

        res.status(200).json({ total_bill: totalBill });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});

app.get('/service/calculate_bill', async (req, res) => {
    const collection = db.collection('Service');
    try {
        const services = await collection.find({}).toArray();
        let totalBill = 0;

        services.forEach(service => {
            const price = service.price;
            const tax = calculateServiceTax(price);
            const totalPrice = price + tax;
            totalBill += totalPrice;
        });

        res.status(200).json({ total_bill: totalBill });
    } catch (err) {
        res.status(500).json({ message: err.message });
    }
});



app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});