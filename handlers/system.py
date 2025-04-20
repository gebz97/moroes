from models import System

def create_handler(args, session, vault):
    sys = System(name=args.name)
    session.add(sys)
    session.commit()
    print(f"Created System id={sys.id} name={sys.name}")

def list_handler(args, session, vault):
    for s in session.query(System).all():
      print(f"{s.id}\t{s.name}")

def update_handler(args, session, vault):
    sys = session.query(System).get(args.id)
    sys.name = args.name
    session.commit()
    print(f"Updated System id={sys.id}")

def delete_handler(args, session, vault):
    sys = session.query(System).get(args.id)
    session.delete(sys)
    session.commit()
    print(f"Deleted System id={args.id}")
