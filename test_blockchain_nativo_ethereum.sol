// SPDX-License-Identifier: MIT
// CÓDIGO GENERADO POR VADER 7.0 UNIVERSAL BLOCKCHAIN
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract VaderToken is ERC20, Ownable {
    uint256 public maxSupply;
    uint256 public mintPrice;
    bool public mintingActive;
    
    mapping(address => uint256) public stakingRewards;
    
    event TokenMinted(address indexed to, uint256 amount);
    event TokenBurned(address indexed from, uint256 amount);
    event Staked(address indexed user, uint256 amount);
    
    constructor(string memory name, string memory symbol, uint256 _maxSupply) 
        ERC20(name, symbol) {
        maxSupply = _maxSupply;
        mintingActive = true;
    }
    
    function mint(address to, uint256 amount) public onlyOwner {
        require(mintingActive, "Minting not active");
        require(totalSupply() + amount <= maxSupply, "Max supply exceeded");
        _mint(to, amount);
        emit TokenMinted(to, amount);
    }
    
    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
        emit TokenBurned(msg.sender, amount);
    }
    
    function stake(uint256 amount) public {
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");
        _transfer(msg.sender, address(this), amount);
        stakingRewards[msg.sender] += amount;
        emit Staked(msg.sender, amount);
    }
    
    function unstake(uint256 amount) public {
        require(stakingRewards[msg.sender] >= amount, "Insufficient staked");
        stakingRewards[msg.sender] -= amount;
        _transfer(address(this), msg.sender, amount);
    }
    
    function setMintingActive(bool _active) public onlyOwner {
        mintingActive = _active;
    }
}