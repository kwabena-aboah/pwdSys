export function encrypt(text) {
	return btoa(text)
}

export function decrypt(text) {
	return atob(text)
}