import { db } from '../db'

export async function logAction(action, data) {
	const dbx =  await db
	await dbx.put('logs', {
		id: Date.now(),
		action,
		data,
		time: new Date().toISOString()
	})
}