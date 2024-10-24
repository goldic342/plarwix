import Layout from '../components/ui/Layout'
import LoginPage from '../pages/LoginPage'

export const publicRoutes = [
	{
		path: '/',
		element: <Layout />,
		children: [
			{
				path: '/login',
				element: <LoginPage />,
			},
		],
	},
]
