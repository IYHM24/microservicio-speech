import express from "express";
import { PORT } from "./constantes.js";
import logger from "../components/logger/logger.js";

const app = express();
app.use(express.json());

app.get("/", (req, res) => {
  res.json({ message: "API funcionando 🚀" });
});

app.listen(PORT, () => {
  logger.info(`Servidor escuchando en el puerto ${PORT}`);
});

export default app;