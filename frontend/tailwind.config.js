/** @type {import('tailwindcss').Config} */
export default {
	content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
	theme: {
		extend: {
			colors: {
				primary: 'var(--primary)',
				secondary: 'var(--secondary)',
				span: 'var(--span)',
				accent: 'var(--accent)',
			},
		},
		container: {
			padding: {
				DEFAULT: '1rem',
				sm: '2rem',
			},
			center: true,
		},
	},
	plugins: [],
}
