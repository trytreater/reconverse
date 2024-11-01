from reconverse.main import main
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '-t':
            env = 'testing'
        else:
            print(f"Error: unknown argument \"{sys.argv[1]}\". Exiting.")
            exit(1)
    else:
        env = 'development'

    main(env)