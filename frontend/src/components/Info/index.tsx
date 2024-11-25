import { FC } from 'react'
import { motion } from 'motion/react'

import SectionWrapper from '../../hocs/SectionWrapper'

import useMedia from '../../hoocs/useMedia'
import { fadeIn, inView } from '../../utils'

const infoData = [
	{
		id: 0,
		type: 'IP-адрес',
		description: 'Укажите конкретный IP-адрес',
		example: '192.168.0.1',
	},
	{
		id: 1,
		type: 'Перечисление IP-адресов',
		description: 'Перечислите несколько IP-адресов через пробел',
		example: '192.168.0.1 192.168.0.2',
	},
	{
		id: 2,
		type: 'Диапазон IP-адресов',
		description: 'Задайте диапазон IP-адресов',
		example: '192.168.0.0-192.168.0.255',
	},
	{
		id: 3,
		type: 'CIDR-нотация',
		description:
			'Используйте CIDR-нотацию для сканирования подсетей',
		example: '192.168.0.0/24',
	},
]

const linksData = [
	{
		id: 0,
		href: 'https://nmap.org/man/ru/index.html',
		text: 'Официальная документация Nmap',
	},
	{
		id: 1,
		href: 'https://habr.com/ru/articles/88064/',
		text: 'Книга «Nmap Network Scanning»',
	},
	{
		id: 2,
		href: 'https://securityonion.net/',
		text: 'Веб-сайт Security Onion',
	},
]

const TableDesktop: FC = () => {
	return (
		<div className='overflow-hidden mt-8 flex items-center bg-white rounded-md shadow p-2'>
			<table className='info__table w-full table-fixed'>
				<thead className='text-lg border-b'>
					<motion.tr
						{...inView}
						variants={fadeIn('right', 'spring', 0, 1.2)}>
						<th>Способ задания</th>
						<th>Описание</th>
						<th>Пример</th>
					</motion.tr>
				</thead>
				<tbody className='text-center bg-white'>
					{infoData.map(item => {
						return (
							<motion.tr
								{...inView}
								variants={fadeIn(
									'left',
									'spring',
									0.1 * item.id,
									1.2,
								)}
								key={item.id}>
								<td>
									<strong>{item.type}</strong>
								</td>
								<td>{item.description}</td>
								<td>
									<code
										className='bg-slate-500/20 p-0.5 mx-0.5 rounded cursor-pointer hover:bg-slate-500/30'
										onClick={() =>
											navigator.clipboard.writeText(item.example)
										}>
										{item.example}
									</code>
								</td>
							</motion.tr>
						)
					})}
				</tbody>
			</table>
		</div>
	)
}

const TableMobile: FC = () => {
	return (
		<div>
			{infoData.map(item => {
				return (
					<motion.div
						{...inView}
						variants={fadeIn('right', 'spring', 0, 1.2)}
						key={item.id}>
						<h4 className='mt-8 font-bold text-lg sm:text-xl underline'>
							{item.type}
						</h4>
						<p className='font-medium text-md sm:text-lg mt-2'>
							{item.description}
						</p>
						<p className='mt-1 text-sm sm:text-base'>
							Например:&nbsp;
							<code className='bg-slate-500/20 p-0.5 mx-0.5 rounded cursor-pointer hover:bg-slate-500/30'>
								{item.example}
							</code>
						</p>
					</motion.div>
				)
			})}
		</div>
	)
}

const Info: FC = () => {
	const media768 = useMedia('width<768px')

	return (
		<section className='mt-24 mb-12 text-secondary'>
			<div className='container mx-auto px-4 lg:px-8 xl:px-16'>
				<motion.h3
					{...inView}
					variants={fadeIn('right', 'spring', 0, 1.2)}
					className='font-black text-primary text-2xl sm:text-3xl md:text-3xl leading-tight'>
					Как пользоваться нашим продуктом?
				</motion.h3>
				<motion.p
					{...inView}
					variants={fadeIn('right', 'spring', 0, 1.2)}
					className='mt-2 max-w-[500px]'>
					Воспользуйтесь настройками и введите желаемый адрес в
					одном из форматах, предложенных ниже:
				</motion.p>
				{media768 ? <TableMobile /> : <TableDesktop />}

				<motion.h4
					{...inView}
					variants={fadeIn('right', 'spring', 0, 1.2)}
					className='text-xl font-semibold mt-8'>
					Какие источники можно почитать?
				</motion.h4>
				<motion.ul
					{...inView}
					variants={fadeIn('right', 'spring', 0, 1.2)}
					className='flex flex-col pl-2 mt-2 gap-3'>
					{linksData.map(link => (
						<li key={link.id}>
							<a
								target='_blank'
								className='text-md text-blue-500 hover:underline'
								href={link.href}>
								{link.text}
							</a>
						</li>
					))}
				</motion.ul>
			</div>
		</section>
	)
}
const infoSection = SectionWrapper(Info, 'info')

export default infoSection
