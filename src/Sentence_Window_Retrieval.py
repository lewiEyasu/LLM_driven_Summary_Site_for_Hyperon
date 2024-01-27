import pandas as pd


def sentence_window(path, index, window_size):
    """
    Extracts a window of text around a given index.

    Args:
        path (str): The path for the dataset.csv file .
        index (int): The index of the center word in the window.
        window_size (int): The size of the window (half the number of words to extract
            on either side of the center word).

    Returns:
        str: The extracted window of text.

    Raises:
        TypeError: If any of the input arguments are not of the expected types.
        ValueError: If the window size is less than 1.
    """

    try:
        df = pd.read_csv(path)
    except Exception as err:
        print("can't open the cvs file from the given path\nError message: ", err) 
    else:
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")

        if not isinstance(window_size, int):
            raise TypeError("Window size must be an integer.")

        if window_size < 1:
            raise ValueError("Window size must be at least 1.")
        
        print(df['text'][index], '\n\n\n')
        start_index = max(0, index - window_size)
        end_index   = min(len(df['text']), index + window_size + 1)

        return (df['text'][start_index:end_index]).to_string(index=False)
