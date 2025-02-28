# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Test case 1: ui_in = 170 (0b10101010), uio_in = 204 (0b11001100)
    dut.ui_in.value = 0b10101010
    dut.uio_in.value = 0b11001100
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b10001000, f"Test case 1 failed: Expected 0b10001000, got {dut.uo_out.value}"

    # Test case 2: ui_in = 255 (0b11111111), uio_in = 255 (0b11111111)
    dut.ui_in.value = 0b11111111
    dut.uio_in.value = 0b11111111
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b11111111, f"Test case 2 failed: Expected 0b11111111, got {dut.uo_out.value}"

    # Test case 3: ui_in = 0 (0b00000000), uio_in = 255 (0b11111111)
    dut.ui_in.value = 0b00000000
    dut.uio_in.value = 0b11111111
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00000000, f"Test case 3 failed: Expected 0b00000000, got {dut.uo_out.value}"

    # Test case 4: ui_in = 170 (0b10101010), uio_in = 85 (0b01010101)
    dut.ui_in.value = 0b10101010
    dut.uio_in.value = 0b01010101
    await ClockCycles(dut.clk, 1)
    assert dut.uo_out.value == 0b00000000, f"Test case 4 failed: Expected 0b00000000, got {dut.uo_out.value}"

    dut._log.info("All test cases passed!")
