import uuid

def generate_transaction_id():
  """
  Menghasilkan ID transaksi unik menggunakan UUID.
  """
  return str(uuid.uuid4())