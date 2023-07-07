from typing import Any

def get_input(prompt:str=">>> ", retry:bool= True, target_type:Any = str) ->Any:
    """
    Get and return user inputs after validate them.
    |
    Arguments:
    prompt= a string to show user as a guide. | 
    retry= a boolian which is use for getting input until a valid one; Defualt is True |
    target_type= a callable type, use for return inputs in its type; Default is str
    |
    example:
    get_input(prompt = "input a number: ", retry= True, target_type= int)
    """
    try:
        assert callable(target_type), f"{target_type} is not callable."

        user_input = input(prompt)
        user_input = target_type(user_input)

    except KeyboardInterrupt as err:
        print(f"\nForce Exit\nReason: {err}")
        exit(0)
    except AssertionError as err:
        print(f"AssertionError: {err}")
    except Exception as err:
        if retry:
            print("Invalid input, try again. [Ctrl+c to exit.]")
            return get_input(prompt, retry, target_type)
        else:
            print(f"Invalid input.\nError raise: {err}")
        return user_input