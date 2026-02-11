import instance from './api/axios';
import { db } from '../db'
import { logAction } from '../logs/audit'

export async function savePWD(data) {
	if(!navigator.online) {
		const dbx = await db
		await dbx.put('records', {
			...data,
			local_id: Date.now(),
			status: 'pending'
		})

		await logAction("OFFLINE_SAVE", data)
		return { offline: true }
	}

	await instance.post('/pwd_records/', data)
	await logAction('ONLINE_SAVE', data)
}