from models import Server

def create_handler(args, session, vault):
  srv = Server(
    hostname=args.name,
    ip_address=args.ip_address,
    service_id=args.service_id
  )
  session.add(srv)
  session.commit()
  print(f"Created Server id={srv.id} host={srv.hostname}")

def list_handler(args, session, vault):
  for s in session.query(Server).all():
    print(f"{s.id}\t{s.hostname}\t{ s.ip_address }\tSvc={s.service_id}")

def update_handler(args, session, vault):
  srv = session.query(Server).get(args.id)
  if args.name:
    srv.hostname = args.name
  if args.ip_address:
    srv.ip_address = args.ip_address
  session.commit()
  print(f"Updated Server id={srv.id}")

def delete_handler(args, session, vault):
  srv = session.query(Server).get(args.id)
  session.delete(srv)
  session.commit()
  print(f"Deleted Server id={args.id}")
