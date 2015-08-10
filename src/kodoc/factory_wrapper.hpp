// Copyright Steinwurf ApS 2014.
// Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
// See accompanying file LICENSE.rst or
// http://www.steinwurf.com/licensing

#pragma once

#include "kodo_factory.hpp"

namespace kodo
{
    template<class KodoStack>
    class factory_wrapper : public kodo_factory
    {
    public:
        factory_wrapper(uint32_t max_symbols, uint32_t max_symbol_size) :
            m_factory(max_symbols, max_symbol_size)
        { }

        virtual void set_symbols(uint32_t symbols)
        {
            m_factory.set_symbols(symbols);
        }

        virtual void set_symbol_size(uint32_t symbol_size)
        {
            m_factory.set_symbol_size(symbol_size);
        }

        virtual uint32_t max_symbols() const
        {
            return m_factory.max_symbols();
        }

        virtual uint32_t max_symbol_size() const
        {
            return m_factory.max_symbol_size();
        }

        virtual uint32_t max_block_size() const
        {
            return m_factory.max_block_size();
        }

        virtual uint32_t max_payload_size() const
        {
            return m_factory.max_payload_size();
        }

    protected:

        typename KodoStack::factory m_factory;
    };
}
