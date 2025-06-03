import sys
from datetime import datetime
from commands import check_latency, check_availability, render_graph
from logger import setup_logger

logger = setup_logger()

def parse_command(command_str):
    """
    Parsear el comando de texto en tokens
    """
    tokens = command_str.strip().split()
    return tokens

def run_command(tokens):
    """
    Ejecuta el comando según los tokens
    """
    if not tokens:
        print("No command entered.")
        return

    cmd = tokens[0].lower()
    args = tokens[1:]

    if cmd == "checklatency":
        module = args[0] if args else 'all'
        logger.info(f"Executing CheckLatency for module: {module}")
        result = check_latency.check_latency(module)
        print(result)

    elif cmd == "checkavailability":
        module = args[0] if args else 'all'
        logger.info(f"Executing CheckAvailability for module: {module}")
        result = check_availability.check_availability(module)
        print(result)

    elif cmd == "rendergraph":
        if len(args) < 1:
            print("Usage: RenderGraph <metric> [module] [period]")
            return
        metric = args[0]
        module = args[1] if len(args) > 1 else 'all'
        period = args[2] if len(args) > 2 else 'Last5Days'
        logger.info(f"Executing RenderGraph with metric={metric}, module={module}, period={period}")
        result = render_graph.render_graph(metric, module, period)
        print(result)

    else:
        print(f"Unknown command: {cmd}")

def main():
    print("Bot MonitorMach started. Enter commands or 'exit' to quit.")
    while True:
        try:
            command_str = input(">> ")
            if command_str.lower() in ('exit', 'quit'):
                print("Exiting bot.")
                break

            tokens = parse_command(command_str)
            run_command(tokens)

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting bot.")
            break
        except Exception as e:
            logger.error(f"Error running command: {str(e)}")

if __name__ == "__main__":
    main()
