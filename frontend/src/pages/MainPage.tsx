import { type FC } from 'react'

import { MainLayout } from '../layouts'

import { Hero, Info, Main } from '../components'

const MainPage: FC = () => {
	return (
		<MainLayout>
			<Hero />
			<Main />
			<Info />
		</MainLayout>
	)
}
export default MainPage
