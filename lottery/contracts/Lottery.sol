//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";


contract Lottery is Ownable{
    enum State {CLOSED, ONGOING, PICKING_WINNER}

    address payable [] public participants;
    mapping(address => uint256) participantWeight;

    State public gameState;
    uint256 minAmountUSD;

    AggregatorV3Interface priceFeed;

    modifier AtLeastMinAmountUSD() {
        //todo: require for min amount
        _;
    }
    modifier OnGoingGame() {
        require(gameState == State.ONGOING, "An Ongoing Game is required to bet");
        _;
    }

    function bet() public payable AtLeastMinAmountUSD OnGoingGame{
        participants.push(payable(address (msg.sender)));
        participantWeight[address(msg.sender)] = msg.value;
    }

    function getEntryMinEth() public view returns(uint256) {
        (,int price,,,) = priceFeed.latestRoundData();
        uint256 tempMin = minAmountUSD * 10 ** 18;
        uint256 minEth = tempMin / ( uint256(price) * 10 ** 10);
        return minEth;
    }

    constructor(address priceFeedAddress) {
        priceFeed = AggregatorV3Interface(priceFeedAddress);
        gameState = State.CLOSED;
        minAmountUSD = 50 * 10 ** 18;
    }

    function startLottery() public onlyOwner {
        require(gameState != State.ONGOING, "Game Already Started");
        gameState = State.ONGOING;
    }
}
