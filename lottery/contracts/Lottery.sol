//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Lottery {
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

    function bet(uint256 amount) public payable AtLeastMinAmountUSD OnGoingGame{
        participants.push(payable(address (msg.sender)));
        participantWeight[address(msg.sender)] = msg.value;
    }

    constructor() public {
        gameState = State.CLOSED;
        minAmountUSD = 50 * 10 ** 18;
    }

    function startLottery() public {
        require(gameState != State.ONGOING, "Game Already Started");
        gameState = State.ONGOING;
    }
}
