import { appExpress } from './src/config/constantes.js';
import registerHealthRoutes from './src/Routes/health.routes.js';

// Registrar rutas
registerHealthRoutes(appExpress); // Rutas de salud
