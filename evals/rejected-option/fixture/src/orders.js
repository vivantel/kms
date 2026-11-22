// GET /orders: reads straight from Postgres, paginated.
export async function listOrders(db, { limit = 50, offset = 0 } = {}) {
  return db.query('SELECT * FROM orders ORDER BY id LIMIT $1 OFFSET $2', [limit, offset]);
}
