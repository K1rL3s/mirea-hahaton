import { useEffect, useState } from 'react'

const useMedia = (query: string) => {
	const [matches, setMatches] = useState<boolean>(true)
	query = `(${query})`

	const handleChange = () =>
		setMatches(window.matchMedia(query).matches)

	useEffect(() => {
		handleChange()

		const matchMedia = window.matchMedia(query)

		matchMedia.addEventListener('change', handleChange)

		return () =>
			matchMedia.removeEventListener('change', handleChange)
	}, [query])

	return matches
}
export default useMedia
