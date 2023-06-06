import sys
from database import get_connection, add_subscriber

if len(sys.argv) != 4:
    print("Usage: python3 add_new_subscriber.py '<id>' '<name>' <gap>")
    sys.exit(1)

id = sys.argv[1]
name = sys.argv[2]
gap = sys.argv[3]

connection = get_connection()
add_subscriber(connection, id, name, gap)

# python -c "from database import get_connection; connection = get_connection(); connection.execute('''ALTER TABLE suscribers RENAME TO subscribers''')"
