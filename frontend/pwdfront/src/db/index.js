import { openDB } from 'idb'

export const db = openDB('pwd-db', 1, {
	upgrade(db) {
		db.createObjectStore('records', { keyPath: 'local_id' })
		db.createObjectStore('logs', { keyPath: 'id' })
	}
})