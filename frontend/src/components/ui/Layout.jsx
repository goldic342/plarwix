import { Box, Heading } from '@chakra-ui/react'
import { Outlet } from 'react-router-dom'

const Layout = () => {
	return (
		<div>
			<Box as={'header'} bg={'teal.500'} p={3}>
				<Heading fontSize={'lg'} fontWeight={'semibold'} color={'white'}>
					Plarwix
				</Heading>
			</Box>
			<Outlet />
		</div>
	)
}

export default Layout
