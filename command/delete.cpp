#include "commands.hpp"

#include <filesystem>
#include <string>
#include <vector>
using namespace std;

#include "utils/logger.hpp"

/**
 * @brief Deletes the config associated to a device,
 * without causing error if the config does not exists.
 *
 * @param path to the infrared camera, empty string to execute all configs
 *
 * @return exit code
 */
ExitCode delete_config(const char* device)
{
    Logger::debug("Executing delete command.");

    vector<string> configs = GetConfigPaths(device);
    for (auto &config : configs) {
        Logger::debug("Deleting", config);
        filesystem::remove(config);
    }

    Logger::info("The configurations have been deleted.");
    return ExitCode::SUCCESS;
}
