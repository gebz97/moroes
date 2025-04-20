from models import Service, System

def create_handler(args, session, vault):
  svc = Service(name=args.name, system_id=args.system_id)
  session.add(svc)
  session.commit()
  print(f"Created Service id={svc.id} name={svc.name}")

def list_handler(args, session, vault):
  for svc in session.query(Service).all():
    print(f"{svc.id}\t{svc.name}\tSystem={svc.system_id}")

def update_handler(args, session, vault):
  svc = session.query(Service).get(args.id)
  svc.name = args.name
  session.commit()
  print(f"Updated Service id={svc.id}")

def delete_handler(args, session, vault):
  svc = session.query(Service).get(args.id)
  session.delete(svc)
  session.commit()
  print(f"Deleted Service id={args.id}")
