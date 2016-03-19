import random
import unittest
import math
import numpy

from hammoudeh_puzzle_solver.puzzle_importer import Puzzle
from hammoudeh_puzzle_solver.puzzle_piece import PuzzlePiece


class PuzzleTester(unittest.TestCase):
    PIECE_WIDTH = 5
    NUMB_PUZZLE_PIECES = 9
    NUMB_PIXEL_DIMENSIONS = 3

    TEST_ARRAY_FIRST_PIXEL_VALUE = 0

    # Get the information on the test image
    TEST_IMAGE_FILENAME = ".\\test\\test.jpg"
    TEST_IMAGE_WIDTH = 300
    TEST_IMAGE_HEIGHT = 200

    def test_puzzle_creation(self):
        """
        Puzzle Import Parameter Checker

        Checks that for an image, the parameters of the image are successfully parsed.
        """
        test_img_id = 999

        # Create a dummy image for testing purposes
        Puzzle.DEFAULT_PIECE_WIDTH = PuzzleTester.PIECE_WIDTH
        puzzle = Puzzle(test_img_id, PuzzleTester.TEST_IMAGE_FILENAME)

        # Verify the test image id number
        assert(puzzle._id == test_img_id)

        # Verify the piece width information
        assert(puzzle._piece_width == PuzzleTester.PIECE_WIDTH)

        # Verify the image filename information
        assert(puzzle._filename == PuzzleTester.TEST_IMAGE_FILENAME)

        # Verify the image size info
        assert(puzzle._img_height == PuzzleTester.TEST_IMAGE_HEIGHT)
        assert(puzzle._img_width == PuzzleTester.TEST_IMAGE_WIDTH)

        # Verify the grid side is correct
        assert(puzzle._grid_size == (PuzzleTester.TEST_IMAGE_HEIGHT / PuzzleTester.PIECE_WIDTH,
                                     PuzzleTester.TEST_IMAGE_WIDTH / PuzzleTester.PIECE_WIDTH))

        # Verify the number of pieces are correct.
        assert(len(puzzle._pieces) == (PuzzleTester.TEST_IMAGE_HEIGHT / PuzzleTester.PIECE_WIDTH) *
               (PuzzleTester.TEST_IMAGE_WIDTH / PuzzleTester.PIECE_WIDTH))

        # Check information about the piece
        all_pieces = puzzle.pieces  # type: [PuzzlePiece]
        for piece in all_pieces:
            assert(piece.width == PuzzleTester.PIECE_WIDTH)

            assert(piece._orig_puzzle_id == test_img_id)
            assert(piece._assigned_puzzle_id is None)

            assert(piece.rotation is None)  # No rotation by default

            rand_loc = (random.randint(0, 9999), random.randint(0, 9999))
            piece.location = rand_loc
            assert(piece.location == rand_loc)
            piece._assign_to_original_location()
            assert(piece._orig_loc == piece.location)

    def test_puzzle_piece_maker(self):
        """
        Puzzle Piece Maker Checker

        Checks that puzzle pieces are made as expected.  It also checks the get puzzle piece row/column values.
        """

        # Create a puzzle whose image data will be overridden
        puzzle = Puzzle(0, PuzzleTester.TEST_IMAGE_FILENAME)

        # Build a dummy image for testing.
        img = PuzzleTester.build_dummy_array()
        img_shape = img.shape

        # Overwrite the image parameters
        puzzle._img = img
        puzzle._img_LAB = img
        puzzle._img_width = img_shape[1]
        puzzle._img_height = img_shape[0]
        puzzle._piece_width = PuzzleTester.PIECE_WIDTH
        puzzle._grid_size = (math.sqrt(PuzzleTester.NUMB_PUZZLE_PIECES), math.sqrt(PuzzleTester.NUMB_PUZZLE_PIECES))

        # Remake the puzzle pieces
        puzzle.make_pieces()

        # Get the puzzle pieces
        pieces = puzzle.pieces
        # Get the first piece
        first_piece = pieces[0]  # type: PuzzlePiece

        # Test the Extraction of row pixel values
        for row in range(0, PuzzleTester.PIECE_WIDTH):
            first_dim_val = PuzzleTester.TEST_ARRAY_FIRST_PIXEL_VALUE + row * PuzzleTester.row_to_row_step_size()

            # Test the extraction of pixel values.
            test_arr = PuzzleTester.build_pixel_list(first_dim_val, True)
            row_val = first_piece.get_row_pixels(row)
            assert(numpy.array_equal(row_val, test_arr))  # Verify the two arrays are equal.

            # Test the reversing
            reverse_list = True
            test_arr = PuzzleTester.build_pixel_list(first_dim_val, True, reverse_list)
            row_val = first_piece.get_row_pixels(row, reverse_list)
            assert(numpy.array_equal(row_val, test_arr))

    @staticmethod
    def build_pixel_list(start_value, is_row, reverse_list=False):
        """
        Pixel List Builder

        Given a starting value for the first pixel in the first dimension, this function gets the pixel values
        in an array similar to a call to "get_row_pixels" or "get_col_pixels" for a puzzle piece.

        Args:
            start_value (int): Value of the first (i.e. lowest valued) pixel's first dimension

            is_row (bool): True if building a pixel list for a row and "False" if it is a column.  This is used to
            determine the stepping factor from one pixel to the next.

            reverse_list (bool): If "True", HIGHEST valued pixel dimension is returned in the first index of the list
            and all subsequent pixel values are monotonically DECREASING.  If "False", the LOWEST valued pixel dimension
            is returned in the first index of the list and all subsequent pixel values are monotonically increasing.

        Returns ([int]): An array of individual values simulating a set of pixels
        """

        # Determine the pixel to pixel step size
        if is_row:
            pixel_offset = PuzzleTester.NUMB_PIXEL_DIMENSIONS
        else:
            pixel_offset = PuzzleTester.row_to_row_step_size()

        # Build the list of pixel values
        pixels = numpy.zeros((PuzzleTester.PIECE_WIDTH, PuzzleTester.NUMB_PIXEL_DIMENSIONS))
        for i in range(0, PuzzleTester.PIECE_WIDTH):
            pixel_start = start_value + i * pixel_offset
            for j in range(0, PuzzleTester.NUMB_PIXEL_DIMENSIONS):
                pixels[i,j] = pixel_start + j

        # Return the result either reversed or not.
        if reverse_list:
            return pixels[::-1]
        else:
            return pixels

    @staticmethod
    def row_to_row_step_size():
        """
        Row to Row Step Size

        For a given pixel's given dimension, this function returns the number of dimensions between this pixel and
        the matching pixel exactly one row below.

        It is essentially the number of dimensions multiplied by the width of the original image (in pixels).

        Returns (int): Offset in dimensions.
        """
        step_size = PuzzleTester.NUMB_PIXEL_DIMENSIONS * PuzzleTester.PIECE_WIDTH * math.sqrt(PuzzleTester.NUMB_PUZZLE_PIECES)
        return int(step_size)

    @staticmethod
    def build_dummy_array():
        """

        Returns:

        """
        # Define the puzzle side
        piece_width = PuzzleTester.PIECE_WIDTH
        numb_pieces = PuzzleTester.NUMB_PUZZLE_PIECES
        numb_dim = PuzzleTester.NUMB_PIXEL_DIMENSIONS

        # Define the array
        arr = numpy.zeros((piece_width * math.sqrt(numb_pieces), piece_width * math.sqrt(numb_pieces), numb_dim))
        # populate the array
        val = PuzzleTester.TEST_ARRAY_FIRST_PIXEL_VALUE
        shape = arr.shape
        for row in range(0, shape[0]):
            for col in range(0, shape[1]):
                for dim in range(0, shape[2]):
                    arr[row, col, dim] = val
                    val += 1
        return arr

if __name__ == '__main__':
    unittest.main()