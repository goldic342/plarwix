import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { publicRoutes } from './routes/routes'

const router = createBrowserRouter(publicRoutes)

const App = () => {
	return <RouterProvider router={router} />
}

export default App
