// SPDX-License-Identifier: MIT

pragma solidity ^0.8;

contract SimpleStorage {
    string[] public _data;

    function saveData(string memory data) public {
        _data.push(data);
    }

    function retrieveAt(uint256 index) public view returns(string memory) {
        return _data[index];
    }

}