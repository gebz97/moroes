from models import Database

def create_handler(args, session, vault):
  db = Database(
    name=args.name,
    version=args.version,
    server_id=args.server_id
  )
  session.add(db)
  session.commit()
  print(f"Created Database id={db.id} name={db.name}")

def list_handler(args, session, vault):
  for d in session.query(Database).all():
    print(f"{d.id}\t{d.name}\tv{d.version}\tSrv={d.server_id}")

def update_handler(args, session, vault):
  db = session.query(Database).get(args.id)
  if args.name:
    db.name = args.name
  if args.version:
    db.version = args.version
  session.commit()
  print(f"Updated Database id={db.id}")

def delete_handler(args, session, vault):
  db = session.query(Database).get(args.id)
  session.delete(db)
  session.commit()
  print(f"Deleted Database id={args.id}")
