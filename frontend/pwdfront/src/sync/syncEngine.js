import instance from './api/axios';
import { db } from '../db'
import { logAction } from '../logs/audit'
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

export async function syncData() {
	if (!navigator.online) return

	const dbx = await db
	const all = await dbx.getAll('records')

	for (let r of all) {
		try {
			await instance.post('/sync/', r)
			await dbx.delete('records', r.local_id)
			await logAction('SYNC_SUCCESS', r)
		} catch (e) {
			console.log('Sync failed, retrying later')
			toast.info('Sync failed, retrying later')
		}
	}
}

window.addEventListener('online', syncData)
setInterval(syncData, 30000)