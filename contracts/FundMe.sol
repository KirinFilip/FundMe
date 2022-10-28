// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import "./PriceConverter.sol";

error FundMe__NotOwner();

contract FundMe {
    using PriceConverter for uint256;

    uint256 public constant MINIMUM_USD = 50 * 1e18;

    address[] public funders;
    mapping(address => uint256) public addressToAmountFunded;
    address public immutable i_owner;

    AggregatorV3Interface public priceFeed;

    modifier onlyOwner() {
        // require(msg.sender == i_owner, "Sender is not owner!");
        if (msg.sender != i_owner) revert FundMe__NotOwner(); // uses less gas
        _;
    }

    constructor(address priceFeedAddress) {
        i_owner = msg.sender;
        priceFeed = AggregatorV3Interface(priceFeedAddress);
    }

    // Function to receive Ether. msg.data must be empty
    receive() external payable {
        fund(); // call fund() to document the sender and check for MINIMUM_USD
    }

    // Fallback function is called when msg.data is not empty
    fallback() external payable {
        fund(); // call fund() to document the sender and check for MINIMUM_USD
    }

    function fund() public payable {
        require(
            msg.value.getConversionRate(priceFeed) > MINIMUM_USD,
            "Not enough ETH!"
        );
        funders.push(msg.sender);
        addressToAmountFunded[msg.sender] += msg.value;
    }

    function withdraw() public payable onlyOwner {
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        funders = new address[](0);
        (bool callSuccess, ) = payable(msg.sender).call{
            value: address(this).balance
        }("");
        require(callSuccess, "Call failed");
    }
}
