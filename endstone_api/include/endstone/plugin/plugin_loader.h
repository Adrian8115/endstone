// Copyright (c) 2023, The Endstone Project. (https://endstone.dev) All Rights Reserved.
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

#include <memory>
#include <string>
#include <vector>

#include "endstone/plugin/plugin.h"
#include "endstone/server.h"

class PluginLoader {
public:
    virtual ~PluginLoader() = default;
    [[nodiscard]] virtual std::unique_ptr<Plugin> loadPlugin(const std::string &file) = 0;
    [[nodiscard]] virtual std::vector<std::string> getPluginFileFilters() const = 0;
    virtual void enablePlugin(Plugin &plugin) const = 0;
    virtual void disablePlugin(Plugin &plugin) const = 0;
    [[nodiscard]] virtual Server &getServer() const = 0;
};