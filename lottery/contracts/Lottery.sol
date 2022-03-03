//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract Lottery is Ownable, VRFConsumerBase {
    enum State {
        CLOSED,
        ONGOING,
        PICKING_WINNER
    }

    address payable[] public participants;
    mapping(address => uint256) public participantWeight;

    State public gameState;
    uint256 minAmountUSD;

    AggregatorV3Interface priceFeed;

    bytes32 internal keyHash;
    uint256 internal fee;

    uint256 public randomResult;

    constructor(
        address _priceFeedAddress,
        address _vrf_coordinator,
        address _link,
        bytes32 _keyHash,
        uint256 _fee
    ) VRFConsumerBase(_vrf_coordinator, _link) {
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
        gameState = State.CLOSED;
        minAmountUSD = 0.01 * 10**18;

        keyHash = _keyHash;
        fee = _fee;
    }

    function bet() public payable AtLeastMinAmountUSD OnGoingGame OnlyOnce {
        participants.push(payable(address(msg.sender)));
        participantWeight[address(msg.sender)] += msg.value;
    }

    function getEntryMinEth() public view returns (uint256) {
        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 tempMin = minAmountUSD * 10**18;
        uint256 minEth = tempMin / (uint256(price) * 10**10);
        return minEth;
    }

    function startLottery() public onlyOwner {
        require(
            gameState != State.ONGOING && gameState != State.PICKING_WINNER,
            "Game Already Started"
        );
        gameState = State.ONGOING;
    }

    function getRandomNumber() public returns (bytes32 requestId) {
        require(
            LINK.balanceOf(address(this)) >= fee,
            "Not enough LINK - fill contract with faucet"
        );
        return requestRandomness(keyHash, fee);
    }

    function endLottery() public onlyOwner returns (address) {
        require(gameState == State.ONGOING, "No ongoing game to end");
        gameState = State.PICKING_WINNER;
        getRandomNumber();
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        randomResult = randomness;
    }

    // function cumulitiveWeights() public view returns (uint256[]) {
    //     return [0];
    // }

    modifier AtLeastMinAmountUSD() {
        string memory _errorMessage = string(
            abi.encodePacked(
                "Min Fee is ",
                uint2str(minAmountUSD / (10**18)),
                "$"
            )
        );
        require(msg.value >= getEntryMinEth(), _errorMessage);
        _;
    }

    modifier OnlyOnce() {
        require(
            participantWeight[address(msg.sender)] == 0,
            "You can join the game only once"
        );
        _;
    }

    modifier OnGoingGame() {
        require(
            gameState == State.ONGOING,
            "An Ongoing Game is required to bet"
        );
        _;
    }

    function uint2str(uint256 _i)
        internal
        pure
        returns (string memory _uintAsString)
    {
        if (_i == 0) {
            return "0";
        }
        uint256 j = _i;
        uint256 len;
        while (j != 0) {
            len++;
            j /= 10;
        }
        bytes memory bstr = new bytes(len);
        uint256 k = len;
        while (_i != 0) {
            k = k - 1;
            uint8 temp = (48 + uint8(_i - (_i / 10) * 10));
            bytes1 b1 = bytes1(temp);
            bstr[k] = b1;
            _i /= 10;
        }
        return string(bstr);
    }
}
