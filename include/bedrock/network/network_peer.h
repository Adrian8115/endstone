// Copyright (c) 2024, The Endstone Project. (https://endstone.dev) All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
#pragma once
#include <chrono>

// Only defined as a class to make sure that name mangling happens the same 
class NetworkPeer {
public:
    enum class Reliability {
        Reliable = 0x0,
        ReliableOrdered = 0x1,
        Unreliable = 0x2,
        UnreliableSequenced = 0x3,
    };
    
    using PacketRecvTimepoint = std::chrono::steady_clock::time_point;
};
