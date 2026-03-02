import type { Express } from 'express';
import { appExpress } from "../config/constantes.js";
import { getHealth } from '../controllers/health.controller.js';

const registerHealthRoutes = (app: Express) => {
  app.get("/", getHealth);
}

export default registerHealthRoutes;

