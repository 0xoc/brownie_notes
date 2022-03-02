//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";


contract Lottery is Ownable{
    enum State {CLOSED, ONGOING, PICKING_WINNER}

    address payable [] public participants;
    mapping(address => uint256) participantWeight;

    State public gameState;
    uint256 minAmountUSD;


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

    constructor() {
        gameState = State.CLOSED;
        minAmountUSD = 50 * 10 ** 18;
    }

    function startLottery() public onlyOwner {
        require(gameState != State.ONGOING, "Game Already Started");
        gameState = State.ONGOING;
    }
}
