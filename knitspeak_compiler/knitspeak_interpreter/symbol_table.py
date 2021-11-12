"""Symbol Table structure holds definitions of stitches and context for number variables"""
from typing import Dict, Union

from knit_graphs.Knit_Graph import Pull_Direction
from knitspeak_compiler.knitspeak_interpreter.cable_definitions import Cable_Definition
from knitspeak_compiler.knitspeak_interpreter.stitch_definitions import Stitch_Definition, Stitch_Lean


class Symbol_Table:
    """
    A class used to keep track of how stitches and number variables have been defined. Includes language defaults
    """

    def __init__(self):
        self._symbol_table: Dict[str, Union[Cable_Definition, Stitch_Definition, int]] = {"k": self._knit(), "p": self._purl(),
                                                                                          "yo": self._yo(), "slip": self._slip()}
        self._decreases()
        self._cables()
        # set current row variable
        self._symbol_table["current_row"] = 0

    def _cables(self):
        # Add cable symbols keyed to their definitions to the symbol table

        # Which side (L or R) crosses in front
        for cross_side in ["l", "r"]:
            # Number of loops crossed to the left (each group of loops can have 1, 2, or 3 loops)
            for left_st_num in range(1, 4):
                # Number of loops crossed to the right (each group of loops can have 1, 2, or 3 loops)
                for right_st_num in range(1, 4):
                    # Purl the left stitches?
                    for left_purl in ["p", ""]:
                        # Purl the right stitches?
                        for right_purl in ["p", ""]:
                            # Compose the cable name using the pieces of the stitch definition
                            cable_name = cross_side + "c" + str(left_st_num) + left_purl +\
                                         "|" + str(right_st_num) + right_purl

                            # Get cable definition arguments for purling left stitches
                            if left_purl == "p":
                                left_pull_dir = Pull_Direction.FtB
                            else:
                                left_pull_dir = Pull_Direction.BtF

                            # Get cable definition arguments for purling right stitches
                            if right_purl == "p":
                                right_pull_dir = Pull_Direction.FtB
                            else:
                                right_pull_dir = Pull_Direction.BtF

                            # Get cable definition arguments for lean
                            if cross_side == "l":
                                lean = Stitch_Lean.Left
                            else:
                                lean = Stitch_Lean.Right

                            # Initialize and store the specified cable definition
                            self._symbol_table[cable_name] = Cable_Definition(
                                left_crossing_loops=left_st_num,
                                right_crossing_loops=right_st_num,
                                left_crossing_pull_direction=left_pull_dir,
                                right_crossing_pull_direction=right_pull_dir,
                                cable_lean=lean
                            )

    def _decreases(self):
        # Map various decrease symbols to corresponding Stitch_Definition in the symbol table
        # Includes entries for: k2tog,k3tog, p2tog, p3tog, skpo, sppo, s2kpo, s2ppo, sk2po, sp2po

        self._symbol_table["k2tog"] = Stitch_Definition(
            pull_direction=Pull_Direction.BtF, cabling_depth=0, offset_to_parent_loops=[0, -1], child_loops=1
        )
        self._symbol_table["k3tog"] = Stitch_Definition(
            pull_direction=Pull_Direction.BtF, cabling_depth=0, offset_to_parent_loops=[0, -1, -2], child_loops=1
        )
        self._symbol_table["p2tog"] = Stitch_Definition(
            pull_direction=Pull_Direction.FtB, cabling_depth=0, offset_to_parent_loops=[0, -1], child_loops=1
        )
        self._symbol_table["p3tog"] = Stitch_Definition(
            pull_direction=Pull_Direction.FtB, cabling_depth=0, offset_to_parent_loops=[0, -1, -2], child_loops=1
        )
        self._symbol_table["skpo"] = Stitch_Definition(
            pull_direction=Pull_Direction.BtF, cabling_depth=0, offset_to_parent_loops=[0, 1], child_loops=1
        )
        self._symbol_table["sppo"] = Stitch_Definition(
            pull_direction=Pull_Direction.FtB, cabling_depth=0, offset_to_parent_loops=[0, 1], child_loops=1
        )
        self._symbol_table["s2kpo"] = Stitch_Definition(
            pull_direction=Pull_Direction.BtF, cabling_depth=0, offset_to_parent_loops=[0, 1, 2], child_loops=1
        )
        self._symbol_table["s2ppo"] = Stitch_Definition(
            pull_direction=Pull_Direction.FtB, cabling_depth=0, offset_to_parent_loops=[0, 1, 2], child_loops=1
        )
        self._symbol_table["sk2po"] = Stitch_Definition(
            pull_direction=Pull_Direction.BtF, cabling_depth=0, offset_to_parent_loops=[-1, 0, 1], child_loops=1
        )
        self._symbol_table["sp2po"] = Stitch_Definition(
            pull_direction=Pull_Direction.FtB, cabling_depth=0, offset_to_parent_loops=[-1, 0, 1], child_loops=1
        )

    @staticmethod
    def _slip() -> Stitch_Definition:
        # Stitch Definition with no child_loops
        return Stitch_Definition(
            pull_direction=Pull_Direction.BtF, cabling_depth=0, offset_to_parent_loops=[0], child_loops=0
        )

    @staticmethod
    def _yo() -> Stitch_Definition:
        # Stitch_Definition that will create a new loop with no parents
        return Stitch_Definition(
            pull_direction=Pull_Direction.BtF, cabling_depth=0, offset_to_parent_loops=[], child_loops=1
        )

    @staticmethod
    def _purl() -> Stitch_Definition:
        # Stitch_Definition that will purl the next available loop (purls are front to back)
        return Stitch_Definition(
            pull_direction=Pull_Direction.FtB, cabling_depth=0, offset_to_parent_loops=[0], child_loops=1
        )

    @staticmethod
    def _knit() -> Stitch_Definition:
        # Stitch_Definition that will knit the next available loop (knits are back to front)
        return Stitch_Definition(
            pull_direction=Pull_Direction.BtF, cabling_depth=0, offset_to_parent_loops=[0], child_loops=1
        )

    def __contains__(self, item: str):
        return item.lower() in self._symbol_table

    def __setitem__(self, key: str, value: Union[int, Stitch_Definition, Cable_Definition]):
        self._symbol_table[key.lower()] = value

    def __getitem__(self, item: str):
        return self._symbol_table[item.lower()]
